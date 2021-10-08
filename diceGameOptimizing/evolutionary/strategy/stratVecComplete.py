import numpy as np
#import strategyRep.stratList as stratList
from diceGameOptimizing.evolutionary.strategy.strat import StrategyAbstact

class StratVecComplete(StrategyAbstact):
	"""
    Implementiert die Strategiedarstellung über größere Vektoren.
    """
	def __init__(self, pips, sides):
		"""Initialisiert neuen Strategie Handler für eine größere Vektor-Strategien."""
		self.pips = pips
		self.sides = sides

	def randomStrategy(self):
		"""
		Erstellt eine zufällige Strategie.
		"""
		ret = [] 
		weights = np.random.normal(0, 0.75, (self.pips+1,(self.pips+1)*(self.sides-1)))
		bias = np.zeros(self.pips+1)
		ret.append(weights)
		ret.append(bias)
		return ret

	def nextMove(self, opponentsMoves, strategy):
		"""
		Gibt den nächsten Zug zurück.
		"""
		opp_moves_mat=[]
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
		v = []
		for i in range(self.pips+1):
			v.append(np.sum(opp_moves_mat*strategy[0][i]))
		v+strategy[1]
		return v.index(max(v))

	def changedStrategy(self, strategy, changeRate):
		"""
		Gibt eine veränderte Strategie zurück.
		"""
		ret = []
		ret.append(strategy[0].copy())
		ret.append(strategy[1].copy())
		add_weight = np.random.randn(self.pips+1,(self.pips+1)*(self.sides-1))

		add_weight *= 1*changeRate

		ret[0]= ret[0]+add_weight

		add_bias = np.random.randn(self.pips+1)
		
		add_bias *= 1
		ret[1] = ret[1]+add_bias

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
stratVecObject = StratVecComplete(3,3)


randStr=stratVecObject.randomStrategy()
print("rand vec strat ", randStr)

print("first", stratVecObject.convertToStratList(randStr))

liste_f=stratVecObject.convertToStratList(randStr)
#print(liste_f,'\n')


for i in range(10):
	f2=stratVecObject.changedStrategy(randStr)
	liste_f2=stratVecObject.convertToStratList(f2)
	print("list", liste_f2)
	diffrence=[]
	for j in range(len(liste_f)):
		diffrence.append(liste_f[j]-liste_f2[j])
	print("dif ", diffrence)
print("rand vec strat", randStr)
print("toList ", stratVecObject.convertToStratList(randStr))
"""