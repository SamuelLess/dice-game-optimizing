import abc
"""
Abstrakte Klasse die notwendige Methoden vorgibt.
Wird verwendet um die einzelnen Arten der Repräsentation Strategien zu implementieren.
Nur für Evolutionäre Suche.
"""
class StrategyAbstact(abc.ABC):
	"""
	Abstrakte Klasse die notwendige Methoden vorgibt.
	Wird verwendet um die einzelnen Arten der Repräsentation Strategien zu implementieren.
	Nur für Evolutionäre Suche.
	"""
	def __init__(self, pips, sides):
		pass
	
	@abc.abstractmethod
	def randomStrategy(self):
		"""
		Erstellt eine zufällige Strategie.
		
		Returns
		---------
		Eine Zufällige Strategie.
		"""
		pass

	@abc.abstractmethod
	def changedStrategy(self, stategy, changeRate):
		"""
		Passt eine gegebene Strategie an.

		Parameters
		---------
		strategy : Any
			Zu ändernde Strategie.
		changeRate : float
			Änderungsrate für die Strategie.
		
		Returns
		---------
		Veränderte Strategie.
		"""
		pass

	@abc.abstractmethod
	def nextMove(self, opponentsMoves, strategy):
		"""
		Bestimmt aus gegnerischem Würfel und einer Strategie den nächsten Zug.
		
		Parameters
		---------
		opponentsMoves : [int]
			Alle bisherigen Züge des Gegners.
		strategy : Any
			Strategie, nach der gespielt werden soll.

		Returns
		---------
		Augenzahl, die gespielt werden soll.
		"""
		pass