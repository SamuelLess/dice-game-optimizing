import numpy as np
#import strategyRep.stratList as stratList
from diceGameOptimizing.evolutionary.strategy.strat import StrategyAbstact

import matplotlib.pyplot as plt

HIDDEN_LAYER_SIZE = 4
ActivationFunc = 0

class StratVecDoubleLayer(StrategyAbstact):
	"""
	Implementiert die Strategiedarstellung über einfache Vektoren.
	"""
	def __init__(self, pips, sides):
		"""
		Initialisiert neuen Strategie Handler für NN-Strategien.
		"""
		self.pips = pips
		self.sides = sides 

	def randomStrategy(self):
		"""
		Erstellt eine zufällige Strategie.
		.. note:: 
			Inputlayer: (s-1)(p+1) Neuronen.
			Gewichte dazwischen: HIDDEN_LAYER_SIZE x (s-1)(p+1)
			Hiddenlayer: HIDDEN_LAYER_SIZE
			Gewichte dazwischen (p+1) x (HIDDEN_LAYER_SIZE)
			Outputlayer: (p+1) Neuronen
		"""
		ret = [] 
		weightsIN_HI = np.random.normal(0, 0.75, (HIDDEN_LAYER_SIZE, (self.sides-1)*(self.pips+1)))
		weightsHI_OUT = np.random.normal(0, 0.75, (self.pips+1, HIDDEN_LAYER_SIZE))
		biasIN_HI = np.array([np.zeros(HIDDEN_LAYER_SIZE)]).T
		biasHI_OUT = np.array([np.zeros(self.pips+1)]).T
		ret.append(weightsIN_HI)
		ret.append(biasIN_HI)
		ret.append(weightsHI_OUT)
		ret.append(biasHI_OUT)
		return ret

	@staticmethod
	def activation(x):
		"""
		Hilfsfunktion. Aktivierungsfunktion Sigmoid.
		"""
		return 1/(1+np.exp(-x))

	def nextMove(self, opponentsMoves, strategy):
        """
        Gibt den nächsten Zug zurück
        """
		opp_moves_mat= []
		for i in range(self.sides-1):
			if(len(opponentsMoves)>i):
				for j in range(self.pips+1):
					if(opponentsMoves[i]==j):
						opp_moves_mat.append(1)
					else:
						opp_moves_mat.append(0)
			else:
				for j in range(self.pips+1):
					opp_moves_mat.append(1/self.pips)
		oppVec = np.array([opp_moves_mat]).T
		mult = (strategy[0]@oppVec) + strategy[1]

		mult = StratVecDoubleLayer.activation(mult)

		out = (strategy[2]@mult) + strategy[3]
		return np.argmax(out)


	def changedStrategy(self, strategy, change):
		"""
		Verändert eine gegebene Strategie und gibt eine neue zurück.
		"""
		ret = []
		ret.append(strategy[0].copy())
		ret.append(strategy[1].copy())
		ret.append(strategy[2].copy())
		ret.append(strategy[3].copy())

		add_weight_1 = np.random.randn(HIDDEN_LAYER_SIZE, (self.sides-1)*(self.pips+1))
		add_weight_2 = np.random.randn(self.pips+1, HIDDEN_LAYER_SIZE)

		add_weight_1 *= change
		add_weight_1 *= change

		ret[0] = ret[0]+add_weight_1
		ret[2] = ret[2]+add_weight_2

		add_bias_1 = np.array([np.random.randn(HIDDEN_LAYER_SIZE)]).T
		add_bias_2 = np.array([np.random.randn(self.pips+1)]).T

		add_bias_1 *= 0.1
		add_bias_2 *= 0.1

		ret[1] = ret[1]+add_bias_1
		ret[3] = ret[3]+add_bias_2

		return ret


	def convertToStratList(self, toConvert):
		"""
		Hilfsfunktion. Umwandlung zu einer Listen-Strategie.
		"""
		tempstrat = stratList.StratList(self.pips, self.sides)
		ret_strat=[]
		for state in tempstrat.STATES:
			ret_strat.append(self.nextMove(np.array(state),toConvert))
		return ret_strat
"""
strathandler = StratVecDoubleLayer(6,3)
randstrat = strathandler.randomStrategy()

print(strathandler.nextMove([0,1], randstrat))

print("rand")
print(randstrat)
print("ch")
print(strathandler.changedStrategy(randstrat, 1))


arr1 = np.random.normal(0, 0.75, (4,8))
arr2 = np.random.normal(0, 0.75, (8,1))
"""