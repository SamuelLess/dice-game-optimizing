
class Agent:
	def __init__(self, game, strategy):
		self.game = game
		self.strategy = strategy

	def reinforce(self, state, nextState, action, reward):
		self.strategy.reinforce(state, nextState, action, reward)

	def nextMove(self, state):
		return self.strategy.nextMove(state)
