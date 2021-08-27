
class Agent:
	def __init__(self, game, strategy):
		self.game = game
		self.strategy = strategy

	def reinforce(self, state, nextState, action, reward):
		self.strategy.reinforce(state, nextState, action, reward)

	def nextMove(self, state):
		return self.strategy.nextMove(state)

	def generationComplete(self):
		self.strategy.epsilon *= self.strategy.epsilonDecay

	def evaluateFitness(self):
		rewards = []
		for _ in range(len(self.game.DICE)):
			oppDice = self.game.start(playInOrder=True, invisibleGame=True)
			agentDice = []
			while not self.game.finished():
				action = self.strategy.bestMove((tuple(oppDice), tuple(agentDice)))
				oppDice, reward = self.game.takeAction(action)
				agentDice.append(action)
			rewards.append(reward)
		return sum(rewards)/len(rewards)

