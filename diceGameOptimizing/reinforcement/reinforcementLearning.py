from diceGameOptimizing.reinforcement.agent import Agent
from diceGameOptimizing.reinforcement.strategy.stratQTable import StratQTable
from tqdm import tqdm
import math

class ReinforcementLearning:
	def __init__(self, game, defaultQValue=0.5, strategyRep=0, 
		alpha=0.9, endAlpha=None, gamma=0.5, epsilon=0.3, endEpsilon=None, epsilonDecay=0.999, 
		timeSteps=100, rewardPointDensity=0.001, output=False):
		"""
		Implementiert das Reinforcement Learning in Form von Q-Learning (ε-greedy).
		Lässt sich durch die `train()` Methode ausführen.
		
		.. todo::
			Besseren Namen für `timeSteps` ausdenken!

		Parameters
		---------
		game : Game
			Environment, das optimiert wird.
		defaultQValue : float
			Standardwert im Q-Table
		strategyRep : int
			Art der Darstellung des Q-Table
		alpha : float
			konstanter Wert α für Q-Learning
		gamma : float
			konstanter Wert γ für Q-Learning
		epsilon : float
			Startwert des ε 
		endEpsilon : float
			Endwert des ε
		epsilonDecay : float
			Faktor, mit dem ε nach jedem Spiel verringert wird
		timeSteps : int
			Anzahl der zu spielenden Spiele
		rewardPointDensity : float
			gibt die Dichte der `rewardPoint`s an
		.. warning::
			Es muss 0 <= `strategyRep` <= 0 gelten.
		.. note::
			Bei Verwendung von `endEpsilon` wird `epsilonDecay` ignoriert!
		.. note::
			Bei zu großen Werten von `defaultQValue` wird stürzt der Algorithmus in eine Depression.
		"""
		if endEpsilon is not None:
			epsilonDecay = (endEpsilon/epsilon)**(1.0/timeSteps)
		if endAlpha is not None:
			alphaDecay = (endAlpha/alpha)**(1.0/timeSteps)
		else:
			alphaDecay = 1
		if strategyRep == 0:
			strategy = StratQTable(game, defaultQValue, alpha, alphaDecay, gamma, epsilon, epsilonDecay)
		else:
			print("ERROR: Keine valide Startegierepräsentation!") 
		self.game = game
		self.timeSteps = timeSteps
		self.rewardPointDensity = rewardPointDensity
		self.agent = Agent(game, strategy)
		self.output = output

	def nextGeneration(self):
		"""Spielt ein Spiel und führt dabei das Q-Learning aus.
		"""
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
		"""Führt Trainingszyklus über `timeSteps` viele Spiele aus.

		Returns
		--------
		rewardPoints : [(int, float)]
			Punkte (insgesamt gespielte Spiele, erreichte Auszahlung)
		"""
		rewardPoints = []
		for i in tqdm(range(self.timeSteps)):
			self.nextGeneration()
			if i % math.ceil((self.timeSteps)/(self.rewardPointDensity*self.timeSteps)) == 0:
				#print(self.agent.strategy.printqtable())
				#print(self.agent.strategy.epsilon)
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