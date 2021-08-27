import numpy as np
import random as rand
from tqdm import tqdm
import time

def argNmax(a, N, axis=None):
    return np.take(np.argsort(a, axis=axis), -N)

class StratQTable:
	def __init__(self, game, defaultQValue, alpha, gamma, epsilon, epsilonDecay):
		self.game = game
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.epsilonDecay = epsilonDecay
		self.movesGiven = [0] * (self.game.pips+1)
		self.defaultQValue = defaultQValue
		#qtable wird während des spielens generiert
		self.qtable = {}#{state: (np.full(self.game.pips+1, defaultQValue)) for state in self.STATES}
		#self.generateQTable(defaultQValue)
		#print(self.qtable)

	def reinforce(self, state, nextState, action, reward):
		if state not in self.qtable:
			self.qtable[state] = np.full(self.game.pips+1, self.defaultQValue)
		if nextState not in self.qtable:
			self.qtable[nextState] = np.full(self.game.pips+1, self.defaultQValue)

		q_max = max(self.qtable[nextState]) if len(nextState[0]) < self.game.sides else 0
		"""
		if q_max == 0:
			print("qmax0", nextState)
			print(reward)
			print("before", self.qtable[state][action])
			print("add", (self.alpha * (reward + (self.gamma * q_max) - self.qtable[state][action])))
		"""
		self.qtable[state][action] = self.qtable[state][action] + (self.alpha * (reward + (self.gamma * q_max) 
			- self.qtable[state][action]))
	
	def nextMove(self, state):
		if state not in self.qtable:
			self.qtable[state] = np.full(self.game.pips+1, self.defaultQValue)
		return self.nthBestMove(state, 1)
		"""
		return (np.argmax(self.qtable[state]) if rand.random() > self.epsilon
		else self.nthBestMove(state, 2))
		"""

	def nthBestMove(self, state, nth):
		self.movesGiven[nth] += 1
		if nth == self.game.pips:
			return argNmax(self.qtable[state], nth)
		return (argNmax(self.qtable[state], nth) if rand.random() > self.epsilon 
		else self.nthBestMove(state, nth+1))

	def bestMove(self, state):
		if state not in self.qtable:
			self.qtable[state] = np.full(self.game.pips+1, self.defaultQValue)
		return np.argmax(self.qtable[state])

	def generateQTable(self, defaultQValue):
		"""
		TODO: unreachable state exist; game is finished with only one illegal move 
		"""
		agentDice = [[]]
		for _ in range(self.game.sides-1):
			newDice = []
			for dicePart in agentDice:
				if sum(dicePart) <= self.game.pips:
					for pip in range(self.game.pips+1):
						newDice.append(dicePart+[pip])
				else:
					newDice.append(dicePart+[0])
			agentDice = newDice
		ms = time.time()*1000.0
		for i in range(self.game.sides):
			for oppDicePart in [tuple(dice[0:i+1]) for dice in self.game.DICE]:
				for agentDicePart in [tuple(dice[0:i]) for dice in agentDice]:
					self.qtable[(oppDicePart, agentDicePart)] = np.full(self.game.pips+1, defaultQValue)
		print(f"{len(self.qtable.keys())} states generated in {int((time.time()*1000.0)-ms)}ms")