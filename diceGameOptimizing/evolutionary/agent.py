class Agent:
	def __init__(self, game, strategyHandler, strat, changeRate):
		self.strategyHandler = strategyHandler
		self.game = game
		if strat == 0:
			self.strat = strategyHandler.randomStrategy()
		else:
			self.strat = strat
		self.changeRate = changeRate
		self.fitness = 0
		self.isLegal = True

	def evaluateFitness(self, fitnessAgainst, output=False):
		rewards = []
		if fitnessAgainst == "all":
			for i in range(len(self.game.DICE)):
				oppdice = self.game.start(playInOrder=True)
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
		return Agent(self.game, self.strategyHandler, 
			self.strategyHandler.changedStrategy(self.strat, self.changeRate), self.changeRate)