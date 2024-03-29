import random

class AI:
	def __init__(self, paddle, terminal_side):
		self.__paddle = paddle
		self.__terminal_side = terminal_side
		self.__actions_cost = {'up': -0.001, 'down': -0.001, 'stay': -0.0005}
		self.__q_table = dict()
		self.__memory = dict()
		self.__learning_coef = 0.8
		self.__discount_factor = 0.8
		self.__learn_count = 0
		self.__hit_memory = []
		self.__hit_rate = 0
		self.__first_converge = False
		self.__toggle_first_converge = True

	### getter --------------------------------------------------------------
	def get_states(self):
		states_count = len(self.__q_table)
		print('---------------------------------------------------------')
		print(f'Now have {states_count} state')
		state_sample = [state for state in self.__q_table]
		for i in range(1, 4):
			print(state_sample[-i], self.__q_table[state_sample[-i]])

	def get_learn_count(self):
		return self.__learn_count

	def get_hit_rate(self):
		return self.__hit_rate

	def get_first_converge(self):
		return self.__first_converge

	### setter ---------------------------------------------------------------
	def set_values(self, alpha, gamma):
		self.__learning_coef = alpha
		self.__discount_factor = gamma

	def init_util(self, state):
		self.__q_table[state] = {action: 0 for action in self.__actions_cost}

	def reset_first_converge(self):
		self.__first_converge = False

	def reset(self):
		self.__q_table = dict()
		self.__memory = dict()
		self.__learn_count = 0
		self.__hit_memory = []
		self.__hit_rate = 0
		self.__first_converge = False
		self.__toggle_first_converge = True

	def calculate_hit_rate(self):
		learn_count = len(self.__hit_memory)
		if learn_count != 0:
			if learn_count > 1000:
				self.__hit_memory = self.__hit_memory[-1000:]
				learn_count = 1000
			self.__hit_rate = 100*sum(self.__hit_memory)/learn_count
		else:
			self.__hit_rate = 0
		if (self.__hit_rate == 100.0) and self.__toggle_first_converge and learn_count >= 1000:
			self.__first_converge = True
			self.__toggle_first_converge = False

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
			best_action = random.choice([action for action in self.__actions_cost])

		# perform action
		self.__paddle.perform(best_action)

		self.__memory = {'state': current_state, 'action': best_action}

	# update utility function
	def learn(self, panel_collide_side, paddle_collide, new_state, ball_position_in_danger):
		if new_state not in self.__q_table:
			self.init_util(new_state)

		old_state = self.__memory['state']
		action = self.__memory['action']
		# self.__q_table[old_state][action] = action_reward + state_utility
		
		# reward from doing action
		state_utility = 0
		if panel_collide_side == self.__terminal_side:
			state_utility = -1
			self.__hit_memory.append(0)
		elif paddle_collide:
			state_utility = 1
			self.__hit_memory.append(1)
		elif ball_position_in_danger:
			state_utility = -0.5
		r = self.__actions_cost[self.__memory['action']] + state_utility

		# max possible Q value in new state
		max_value = -1
		for key, value in self.__q_table[new_state].items():
			if value > max_value:
				max_value = value
		new_q_after_discount = self.__discount_factor*max_value

		# Q value of current state
		current_q = self.__q_table[old_state][action]

		# update Q value
		self.__q_table[old_state][action] = current_q + self.__learning_coef * (r + new_q_after_discount - current_q)

		if (panel_collide_side == self.__terminal_side) or paddle_collide:
			self.__learn_count += 1
			self.calculate_hit_rate()