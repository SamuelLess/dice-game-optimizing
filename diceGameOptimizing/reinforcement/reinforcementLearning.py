from diceGameOptimizing.reinforcement.agent import Agent
from diceGameOptimizing.reinforcement.strategy.stratQTable import StratQTable
from tqdm import tqdm
import math

class ReinforcementLearning:
	def __init__(self, game, defaultQValue=0.5, strategyRep=0, 
		alpha=0.9, gamma=0.5, epsilon=0.3, endEpsilon=None, epsilonDecay=0.999, 
		timeSteps=100, rewardPointDensity=0.001, output=False):
		if endEpsilon is not None:
			epsilonDecay = (endEpsilon/epsilon)**(1.0/timeSteps)
		if strategyRep == 0:
			strategy = StratQTable(game, defaultQValue, alpha, gamma, epsilon, epsilonDecay)
		else:
			print("ERROR: Keine valide Startegierepräsentation!") 
		self.game = game
		self.timeSteps = timeSteps
		self.rewardPointDensity = rewardPointDensity
		self.agent = Agent(game, strategy)
		self.output = output

	def nextGeneration(self):
		oppDice = self.game.start()
		agentDice = []
		while not self.game.finished():
			action = self.agent.nextMove((tuple(oppDice), tuple(agentDice)))
			nextOppDice, reward = self.game.takeAction(action)
			#print(f"{agentDice+[action]=}, {nextOppDice=}, {reward=}")
			self.agent.reinforce((tuple(oppDice), tuple(agentDice)), (tuple(nextOppDice), tuple(agentDice+[action])), action, reward)
			agentDice.append(action)
			oppDice = nextOppDice
		self.agent.generationComplete()

	def train(self):
		rewardPoints = []
		for i in tqdm(range(self.timeSteps)):
			self.nextGeneration()
			if i % math.ceil((self.timeSteps)/(self.rewardPointDensity*self.timeSteps)) == 0:
				rewardPoints.append((self.game.gamesPlayed, self.agent.evaluateFitness()))
		if self.output:
			for key in self.agent.strategy.qtable.keys():
				if len(key[0]) > 2:
					continue
				print("state:", key,"\n", self.agent.strategy.qtable[key])
			print("epsilon:",self.agent.strategy.epsilon)
			print("states:", len(self.agent.strategy.qtable.keys()))
		print("movesGiven", self.agent.strategy.movesGiven)
		return rewardPoints