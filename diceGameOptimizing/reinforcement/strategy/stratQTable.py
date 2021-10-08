import numpy as np
import random as rand
from tqdm import tqdm
import time

def argNmax(a, N, axis=None):
    return np.take(np.argsort(a, axis=axis), -N)

class StratQTable:
	def __init__(self, game, defaultQValue, alpha, alphaDecay, gamma, epsilon, epsilonDecay):
		"""
		Implementiert eine Q-Table auf Basis eines `dict`.
		
		Parameters
		---------
		game : Game
			Environment, das optimiert wird.
		defaultQValue : float
			Standardwert im Q-Table.
		strategyRep : int
			Art der Darstellung des Q-Table.
		alpha : float
			Konstanter Wert α für Q-Learning.
		alphaDecay: float
			Faktor, mit dem α nach jedem Spiel verringert wird.
		gamma : float
			Konstanter Wert γ für Q-Learning.
		epsilon : float
			Startwert des ε.
		epsilonDecay : float
			Faktor, mit dem ε nach jedem Spiel verringert wird.

		"""
		self.game = game
		self.alpha = alpha
		self.alphaDecay = alphaDecay
		self.gamma = gamma
		self.epsilon = epsilon
		self.epsilonDecay = epsilonDecay
		self.movesGiven = [0] * (self.game.pips+1)
		self.defaultQValue = defaultQValue
		#qtable wird während des spielens generiert (lazy approach)
		self.qtable = {}
		#self.generateQTable(defaultQValue)

	def reinforce(self, state, nextState, action, reward):
		"""
		Update der Q-Funktion.

		Parameters
		---------
		state : ((int,...),(int,...))
			Zustand.
		nextState : ((int,...),(int,...))
			Nächster Zustand.
		action : int
			Gewählte Aktion.
		reward : float
			Erlangte Belohnung.
		"""	
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
		"""
		Wählt nach ε-greedy Strategie den nächsten Zug aus. 
		Erweiterung: Die Aktion mit dem n. größten Wert wird zur Wahrscheinlichkeit (1-ε)^n ausgewählt.
		"""
		if state not in self.qtable:
			self.qtable[state] = np.full(self.game.pips+1, self.defaultQValue)
		return self.nthBestMove(state, 1)

	def nthBestMove(self, state, nth):
		"""
		Rekursive Funktion, um mit Wahrscheinlichkeit ε nicht den `nth` Zug zu wählen.
		"""
		self.movesGiven[nth] += 1
		if nth == self.game.pips:
			return argNmax(self.qtable[state], nth)
		return (argNmax(self.qtable[state], nth) if rand.random() > self.epsilon 
		else self.nthBestMove(state, nth+1))

	def bestMove(self, state):
		"""
		Gibt den besten Zug zurück. (ohne ε-greedy)
		"""
		if state not in self.qtable:
			self.qtable[state] = np.full(self.game.pips+1, self.defaultQValue)
		return np.argmax(self.qtable[state])

	def printqtable(self):
		"""
		Hilfsfunktion. Ausgabe des Q-Table.
		"""
		out = "PRINTING QTABLE\n"
		for key in self.qtable:
			out += "state: " + str(key) + "\n"
			for i in range(self.game.pips+1):
				out += f"rew{i}: {self.qtable[key][i]:.3f} "
			out += "\n"
		return out

	def generateQTable(self, defaultQValue):
		"""
		Hilfsfunktion. Generiert alle keys für den Q-Table. 
		Nicht nötig mit "lazy" Ansatz zur Erstellung.
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