class AI:
	def __init__(self, paddle, init_state):
		self.__paddle = paddle
		self.__actions = ['up', 'down', 'stay']
		self.__states = dict()
		self.init_util(init_state)
		print(self.__states)

	def init_util(self, state):
		self.__states[state] = {action: 0 for action in self.__actions}