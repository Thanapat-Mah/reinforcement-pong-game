import pygame
import math
import random

class GamePanel:
	def __init__(self, rect=[0, 0, 800, 400], block_size=20, background_color=(40, 40, 40), 
		grid_color=(50, 50, 50), grid_enable=True):
		self.__rect = pygame.Rect(*rect)
		self.__block_size = block_size
		self.__block_count = [int(rect[2]/block_size), int(rect[3]/block_size)]
		self.__background_color = background_color
		self.__grid_color = grid_color
		self.__grid_enable = grid_enable
		self.__terminal_state = ['left']

	### setter --------------------------------------------------------------------------------
	def set_center(self, center_point):
		self.__rect.center = center_point

	def set_grid_enable(self, is_enable):
		self.__grid_enable = is_enable

	### getter --------------------------------------------------------------------------------
	def get_rect(self):
		return self.__rect

	def get_block_size(self):
		return self.__block_size

	def add_terminal(self, side):
		if side not in self.__terminal_state:
			self.__terminal_state.append(side)

	def remove_terminal(self, side):
		if side in self.__terminal_state:
			self.__terminal_state.remove(side)

	def get_inner_position(self, side):
		if side == 'left':
			position = (self.__rect.left+3*self.__block_size, self.__rect.centery)
		elif side == 'right':
			position = (self.__rect.right-3*self.__block_size, self.__rect.centery)
		elif side == 'center':
			position = self.__rect.center
		elif side == 'center_block':
			block_col = int((self.__rect.width/2)/self.__block_size)
			block_row = int((self.__rect.height/2)/self.__block_size)
			x = self.__rect.left + (block_col * self.__block_size) + int(self.__block_size/2)
			y = self.__rect.top + (block_row * self.__block_size) + int(self.__block_size/2)
			position = (x, y)
		elif side == 'center_grid':
			block_col = int((self.__rect.width/2)/self.__block_size)
			block_row = int((self.__rect.height/2)/self.__block_size)
			x = self.__rect.left + block_col * self.__block_size
			y = self.__rect.top + block_row * self.__block_size
			position = (x, y)
		elif side == 'grid_button':
			position = (self.__rect.midbottom[0], self.__rect.midbottom[1]+20)
		elif side == 'render_button':
			position = (self.__rect.bottomleft[0], self.__rect.bottomleft[1]+20)
		elif side == 'fast_button':
			position = (self.__rect.midtop[0], self.__rect.midtop[1]-20)
		elif side == 'left_setting':
			position = (self.__rect.midleft[0]-20, self.__rect.midleft[1])
		elif side == 'right_setting':	
			position = (self.__rect.midright[0]+20, self.__rect.midright[1])
		else:
			position = self.__rect.center
		return position

	# return block position (x, y), start from block 1
	def get_block_position(self, object_position, display=None):
		object_x, object_y = object_position
		panel_x, panel_y = self.__rect.topleft
		block_col = math.ceil((object_x-panel_x)/self.__block_size)
		block_row = math.ceil((object_y-panel_y)/self.__block_size)
		block_position = (block_col, block_row)

		if display:
			# hilight block of object
			block_x = panel_x + (block_col-1)*self.__block_size
			block_y = panel_y + (block_row-1)*self.__block_size
			pygame.draw.rect(display, (120, 60, 60), (block_x, block_y, self.__block_size, self.__block_size), 2)
			pygame.display.update()
			print(block_position)

		return block_position

	# return current state of the game (position of AI paddle and ball)
	def get_state(self, ball, paddle):
		ball_position = self.get_block_position(ball.get_center())
		paddle_position = self.get_block_position(paddle.get_center())
		state_key = f'{ball_position[0]:04d}-{ball_position[1]:04d}_{paddle_position[1]:04d}'
		# print(state_key)
		return state_key

	def check_collision(self, ball):
		collide_sides = []
		# check if ball colide top side wall
		if ball.get_position('top') <= self.__rect.top: collide_sides.append('top')
		if ball.get_position('left') <= self.__rect.left: collide_sides.append('left')
		if ball.get_position('right') >= self.__rect.right: collide_sides.append('right')
		if ball.get_position('bottom') >= self.__rect.bottom: collide_sides.append('bottom')
		
		# if collide with terminal state (wall), restart the ball
		if len(collide_sides) > 0:
			for side in collide_sides:
				if side in self.__terminal_state:
					ball_position = (0, 0)
					if ball.get_is_respawn_center():
						ball_position = self.get_inner_position(side='center_grid')
					else:
						# random new position of ball
						ball_x = random.randint(self.__rect.left, self.__rect.right)
						ball_y = random.randint(self.__rect.top, self.__rect.bottom)
						# snap position to the grid
						panel_x, panel_y = self.__rect.topleft
						block_col = math.ceil((ball_x-panel_x)/self.__block_size)
						block_row = math.ceil((ball_y-panel_y)/self.__block_size)
						ball_x = self.__rect.left + block_col*self.__block_size
						ball_y = self.__rect.top + block_row*self.__block_size
						ball_position = (ball_x, ball_y)
					ball.reset_ball(ball_position)
					return side
				# else change direction
				else:
					ball.change_direction(side)
		return None

	def draw(self, display):
		# draw background
		pygame.draw.rect(display, self.__background_color, self.__rect)

		# draw grid
		if not self.__grid_enable: return None
		top = self.__rect.top
		left = self.__rect.left
		right = self.__rect.right
		bottom = self.__rect.bottom

		# draw vertical grid
		for col in range(1, self.__block_count[0]):
			pygame.draw.line(display, self.__grid_color,
				(left+col*self.__block_size, top),
				(left+col*self.__block_size, bottom))

		# draw horizontal grid
		for row in range(1, self.__block_count[1]):
			pygame.draw.line(display, self.__grid_color,
				(left, top+row*self.__block_size),
				(right, top+row*self.__block_size))