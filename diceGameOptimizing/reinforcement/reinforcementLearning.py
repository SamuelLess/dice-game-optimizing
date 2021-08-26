from diceGame.reinforcement.agent import Agent
from diceGame.reinforcement.strategy.stratQTable import StratQTable

class ReinforcementLearning:
	def __init__(self, game, defaultQValue=0.5, strategyRep=0, alpha=0.9, gamma=0.5, 
		epsilon=0.3, epsilonDecay=0.999, timeSteps=100, output=False):
		if strategyRep == 0:
			strategy = StratQTable(game, defaultQValue, alpha, gamma, epsilon, epsilonDecay)
		else:
			print("ERROR: Keine valide Startegierepräsentation!") 
		self.game = game
		self.timeSteps = timeSteps
		self.agent = Agent(game, strategy)

	def nextGeneration(self):
		oppDice = self.game.start()
		agentDice = []
		while not self.game.finished():
			action = self.agent.nextMove((tuple(oppDice), tuple(agentDice)))
			nextOppDice, reward = self.game.takeAction(action)
			self.agent.reinforce((tuple(oppDice), tuple(agentDice)), (tuple(nextOppDice), tuple(agentDice)), action, reward)
			agentDice.append(action)
			oppDice = nextOppDice

	def train(self):
		for i in range(self.timeSteps):
			self.nextGeneration()
		return [(i,i) for i in range(42)]