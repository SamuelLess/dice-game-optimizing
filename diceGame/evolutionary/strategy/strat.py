import abc
"""
Abstrakte Klasse die notwendige Methoden vorgibt.
Wird verwendet um die einzelnen Arten der Repräsentation Strategien zu implementieren.
Nur für Evolutionäre Suche.
"""
class StrategyAbstact(abc.ABC):
	def __init__(self, pips, sides):
		self.sides = sides

	@abc.abstractmethod
	def randomStrategy(self):
		pass

	@abc.abstractmethod
	def changedStrategy(self, stategy, changeRate):
		pass

	@abc.abstractmethod
	def nextMove(self, opponentsMoves, strategy):
		pass