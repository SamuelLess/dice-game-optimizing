class Agent:
	"""	
	Implementiert einen Agenten für das Evolutionäre Lernen.
	"""
	def __str__(self):
		return str("agent mit " + str(self.fitness) + " ")

	def __init__(self, game, strategyHandler, strat, changeRate):
		"""
		Erstellt einen neuen Agenten.

		Parameters
		---------
		game: Game
			Die Spielinztanz, um die Fitness zu bestimmen.
		strategyHandler: StrategyAbstact
			Handelt die Strategie des Agenten.
		strat : Any
			Strategie, direkt als Liste o. Ä.
		changeRate : float
			Wert, wie stark die Strategie mit jeder Mutation angepasst werden soll.
		"""
		self.strategyHandler = strategyHandler
		self.game = game
		if strat == 0:
			self.strat = strategyHandler.randomStrategy()
		else:
			self.strat = strat
		self.changeRate = changeRate
		self.fitness = 0
		self.isLegal = True

	def evaluateFitness(self, fitnessAgainst, invisibleGame = False, output=False):
		"""Bestimmt die Fitness des Agenten.

		Parameters
		---------
		fitnessAgainst : float | str
			Anteil, gegen wie viele Würfel (Anzahl) von allen gespielt werden soll. Falls "all" wird gegen jeden genau einmal gespielt.
		invisibleGame : bool
			Legt fest, ob das Spiel gezählt wird.
		"""
		rewards = []
		if fitnessAgainst == "all":
			for i in range(len(self.game.DICE)):
				oppdice = self.game.start(playInOrder=True, invisibleGame=invisibleGame)
				while not self.game.finished():
					oppdice, reward = self.game.takeAction(self.strategyHandler.nextMove(oppdice, self.strat))
				rewards.append(reward)
		else:
			for i in range(int(len(self.game.DICE) * fitnessAgainst)):
				oppdice = self.game.start()
				while not self.game.finished():
					oppdice, reward = self.game.takeAction(self.strategyHandler.nextMove(oppdice, self.strat))
				rewards.append(reward)
		if output:
			print(f"{rewards=}")
		self.fitness = sum(rewards)/(len(rewards))
		self.isLegal = True if self.fitness >= 0 else False

	def changedAgent(self):
		"""
		Gibt einen veränderten Agenten zurück.

		Returns
		---------
		Neues Objekt eines veränderten Agenten.
		"""
		return Agent(self.game, self.strategyHandler, 
			self.strategyHandler.changedStrategy(self.strat, self.changeRate), self.changeRate)