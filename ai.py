import random

class AI:
	def __init__(self, paddle, init_state):
		self.__paddle = paddle
		self.__actions = {'up': -0.01, 'down': -0.01, 'stay': -0.1}
		self.__states = dict()
		self.init_util(init_state)
		self.__memory = dict()

	### getter --------------------------------------------------------------
	def get_states(self):
		states_count = len(self.__states)
		print('---------------------------------------------------------')
		print(f'Now have {states_count} state')
		state_sample = [state for state in self.__states]
		for i in range(1, 4):
			print(state_sample[-i], self.__states[state_sample[-i]])


	def init_util(self, state):
		self.__states[state] = {action: 0 for action in self.__actions}

	# select and perform action
	# If best_util_ratio = 1, it always pick the best action
	# else it pick random action
	def perform_action(self, state, best_util_ratio=1):
		if state not in self.__states:
			self.init_util(state)
		current_state = state

		# select best action
		if random.random() <= best_util_ratio:
			best_action = 'stay'
			best_value = self.__states[current_state][best_action]
			for key, value in self.__states[current_state].items():
				if value > best_value:
					best_action = key
					best_value = value
				elif value == best_value:
					best_action = random.choice([best_action, key])
		# select random action
		else:
			best_action = random.choice([action for action in self.__actions])

		# perform action
		self.__paddle.perform(best_action)

		self.__memory = {'state': current_state, 'action': best_action}
		return self.__actions[best_action]

	# update utility function
	def learn(self, action_reward, state_utility):
		old_state = self.__memory['state']
		action = self.__memory['action']
		self.__states[old_state][action] = action_reward + state_utility