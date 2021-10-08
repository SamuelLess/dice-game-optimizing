import numpy as np
from tqdm import tqdm
#import strategyRep.stratList as stratList
import matplotlib.pyplot as plt
from diceGameOptimizing.evolutionary.strategy.strat import StrategyAbstact

class StratVec(StrategyAbstact):
	"""
    Implementiert die Strategiedarstellung über einfache Vektoren.
    """
	def __init__(self, pips, sides):
		"""
        Initialisiert neuen Strategie Handler für einfache Vektor-Strategien.
        """
		self.pips = pips
		self.sides = sides

	def randomStrategy(self):
		"""
		Erstellt eine zufällige Strategie.
		"""
		ret = [] 
		weights = np.random.normal(0, 0.75, (self.pips+1,self.sides-1))
		bias = np.zeros(self.pips+1)
		ret.append(weights)
		ret.append(bias)
		return ret

	def nextMove(self, opponentsMoves, strategy):
		"""
		Gibt den nächsten Zug zurück.
		"""
		opp_moves_mats=[]
		for i in range(self.sides-1):
			if(len(opponentsMoves)>i):
				l=[]
				for j in range(self.pips+1):
					if(opponentsMoves[i]==j):
						l.append(1)
					else:
						l.append(0)
				opp_moves_mats.append(l)
			else:
				l=[]
				for j in range(self.pips+1):
					l.append(1/self.pips)
				opp_moves_mats.append(l)
		opp_moves_mats = np.transpose(opp_moves_mats)
		mult = (opp_moves_mats *strategy[0])
		v = []
		for r in mult:
			v.append(np.sum(r))
		v+strategy[1]
		
		return v.index(max(v))

	def changedStrategy(self, strategy,change):
		"""
		Gibt eine veränderte Strategie zurück.
		"""
		ret = []
		ret.append(strategy[0].copy())
		ret.append(strategy[1].copy())
		add_weight = np.random.randn(self.sides-1,self.pips+1)

		add_weight *= change
		add_weight=np.transpose(add_weight)
		ret[0]= ret[0]+add_weight

		add_bias = np.random.randn(self.pips+1)
		
		add_bias *= 0.5
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
def ave(lst): 
    return sum(lst) / len(lst) 

def pos(lst):
    return [x if x>0 else -x for x in lst]

def bigger(lst,y):
	return [x for x in lst if x>y]

def smaller(lst,y):
	return [x for x in lst if x<y]


def change(i,changeQuantity):
	diffrences=[]
	for i in range(i):
		randStr=stratVecObject.randomStrategy()
		liste_f=stratVecObject.convertToStratList(randStr)	
		f2=stratVecObject.changedStrategy(randStr,changeQuantity)
		liste_f2=stratVecObject.convertToStratList(f2)
		diffrence=[]
		for j in range(len(liste_f)):
			diffrence.append(liste_f[j]-liste_f2[j])
		diffrences.append(sum(pos(diffrence)))

	return ave(diffrences)


def changeFromChangeCoefficient(j,accuracy):
	diffrence=[]

	Max=[]
	Max2=[]
	Min=[]
	Min2=[]
	Ave=[]
	ret=[]
	for i in tqdm(range(j)):
		average=[]
		for l in range(accuracy):
			average.append(change(j,l*(1/accuracy)))
		diffrence.append(average)
	for i in range(accuracy):
		l=[]
		for dif in diffrence:
			l.append(dif[i])
		Ave.append(ave(l))
		Max.append(max(l))
		if(len(bigger(l,ave(l)))>0):
			Max2.append(ave(bigger(l,ave(l))))
		else:
			Max2.append(ave(l))
		Min.append(min(l))
		if(len(smaller(l,ave(l)))>0):
			Min2.append(ave(smaller(l,ave(l))))
		else:
			Min2.append(ave(l))
	ret.append(Ave)
	ret.append(Max)
	ret.append(Min)
	ret.append(Max2)
	ret.append(Min2)
	return ret
"""
"""
for i in range(3,6):
	stratVecObject = StratVec(i,i)

	diffrenceAve=changeFromChangeCoefficient(20,20)

	plt.plot(np.arange(0,1,1/len(diffrenceAve[0])),diffrenceAve[0],label="sides: "+str(i)+", pips: "+str(i))
	#plt.fill_between(np.arange(0,1,1/len(diffrenceAve[0])),diffrenceAve[2],diffrenceAve[1], alpha=0.4)
	plt.fill_between(np.arange(0,1,1/len(diffrenceAve[0])),diffrenceAve[4],diffrenceAve[3], alpha=0.6)
plt.xlabel('changeQuantity')
plt.ylabel('Änderungen')
plt.legend()	
plt.show()
"""