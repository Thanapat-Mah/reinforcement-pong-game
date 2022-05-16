import random

class AI:
	def __init__(self, paddle, init_state):
		self.__paddle = paddle
		self.__actions = {'up': -0.05, 'down': -0.05, 'stay': -0.01}
		self.__q_table = dict()
		self.init_util(init_state)
		self.__memory = dict()
		self.__learning_coef = 0.8
		self.__discount_factor = 0.8

	### getter --------------------------------------------------------------
	def get_states(self):
		states_count = len(self.__q_table)
		print('---------------------------------------------------------')
		print(f'Now have {states_count} state')
		state_sample = [state for state in self.__q_table]
		for i in range(1, 4):
			print(state_sample[-i], self.__q_table[state_sample[-i]])


	def init_util(self, state):
		self.__q_table[state] = {action: 0 for action in self.__actions}

	# select and perform action
	# If best_util_ratio = 1, it always pick the best action
	# else it pick random action
	def perform_action(self, state, best_util_ratio=1):
		if state not in self.__q_table:
			self.init_util(state)
		current_state = state

		# select best action
		if random.random() <= best_util_ratio:
			best_action = 'stay'
			best_value = self.__q_table[current_state][best_action]
			for key, value in self.__q_table[current_state].items():
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
	def learn(self, action_reward, state_utility, new_state):
		if new_state not in self.__q_table:
			self.init_util(new_state)

		old_state = self.__memory['state']
		action = self.__memory['action']
		# self.__q_table[old_state][action] = action_reward + state_utility
		
		# reward from doing action
		r = action_reward + state_utility

		# max possible Q value in new state
		max_value = -1
		for key, value in self.__q_table[new_state].items():
			if value > max_value:
				max_value = value
		bara = self.__discount_factor*max_value

		# Q value of current state
		current_q = self.__q_table[old_state][action]

		# update Q value
		self.__q_table[old_state][action] = current_q + self.__learning_coef * (r + bara - current_q)

q_table = {
	'00_06': {'up': -0.01, 'down': -0.51, 'stay': -0.55},
	'00_01': {'up': -0.01, 'down': -0.51, 'stay': -0.05},
	'00_03': {'up': -0.01, 'down': -0.51, 'stay': -0.55}
}