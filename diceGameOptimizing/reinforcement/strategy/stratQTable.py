import numpy as np
import random as rand
from tqdm import tqdm
import time

def argNmax(a, N, axis=None):
    return np.take(np.argsort(a, axis=axis), -N)

class StratQTable:
	def __init__(self, game, defaultQValue, alpha, alphaDecay, gamma, epsilon, epsilonDecay):
		"""
		Implementiert eine Q-Table auf basis eines `dict`.

		"""
		self.game = game
		self.alpha = alpha
		self.alphaDecay = alphaDecay
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
		if nextState not in self.qtable and len(nextState[0]) < self.game.sides:
			self.qtable[nextState] = np.full(self.game.pips+1, self.defaultQValue)
		
		if len(nextState[0]) == self.game.sides:
			q_max = 0
		else:
			q_max = max(self.qtable[nextState])
		
		self.qtable[state][action] = self.qtable[state][action] + (self.alpha * (reward + (self.gamma * q_max) 
			- self.qtable[state][action]))
	
	def nextMove(self, state):
		if state not in self.qtable:
			self.qtable[state] = np.full(self.game.pips+1, self.defaultQValue)
		return self.nthBestMove(state, 1)

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

	def printqtable(self):
		out = "PRINTING QTABLE\n"
		for key in self.qtable:
			out += "state: " + str(key) + "\n"
			for i in range(self.game.pips+1):
				out += f"rew{i}: {self.qtable[key][i]:.3f} "
			out += "\n"
		return out

	def generateQTable(self, defaultQValue):
		"""
		unused
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