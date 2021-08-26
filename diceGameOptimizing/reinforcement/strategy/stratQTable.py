import numpy as np

class StratQTable:
	def __init__(self, game, defaultQValue, alpha, gamma, epsilon, epsilonDecay):
		self.game = game
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.STATES = []
		self.generateStates()
		self.qtable = {state: ([defaultQValue]*(self.game.pips+1)) for state in self.STATES}
		#print(self.qtable)

	def nextMove(self, state):
		return 0

	def reinforce(self, state, nextState, action, reward):
		pass


	def generateStates(self):
		for i in range(self.game.sides-1):
			for oppDicePart in set(tuple(dice[0:i+1]) for dice in self.game.DICE):
				for agentDicePart in set(tuple(dice[0:i]) for dice in self.game.DICE):
					self.STATES.append((oppDicePart, agentDicePart))
					#print((oppDicePart, agentDicePart))