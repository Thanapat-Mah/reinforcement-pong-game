import pygame

class GamePanel:
	def __init__(self, rect=[0, 0, 800, 500], block_size=20, background_color=(40, 40, 40), 
		grid_color=(50, 50, 50), grid_enable=True):
		self.__rect = pygame.Rect(*rect)
		self.__block_size = block_size
		self.__block_count = [int(rect[2]/block_size), int(rect[3]/block_size)]
		self.__background_color = background_color
		self.__grid_color = grid_color
		self.__grid_enable = grid_enable
		position = (int(self.__rect.width/2), int(self.__rect.height/2))

	### setter --------------------------------------------------------------------------------
	def set_center(self, center_point):
		self.__rect.center = center_point

	### getter --------------------------------------------------------------------------------
	def get_rect(self):
		return self.__rect

	def get_block_size(self):
		return self.__block_size

	def get_inner_position(self, side):
		if side == 'left':
			position = (self.__rect.left+3*self.__block_size, self.__rect.centery)
		elif side == 'right':
			position = (self.__rect.right-3*self.__block_size, self.__rect.centery)
		elif side == 'center':
			position = self.__rect.center
		elif side =='center_block':
			block_col = int((self.__rect.width/2)/self.__block_size)
			block_row = int((self.__rect.height/2)/self.__block_size)
			x = self.__rect.left + (block_col * self.__block_size) + int(self.__block_size/2)
			y = self.__rect.top + (block_row * self.__block_size) + int(self.__block_size/2)
			position = (x, y)
		else:
			position = self.__rect.center
		return position

	def check_collision(self, ball):
		collide_side = False
		# check if ball colide top side wall
		if ball.get_position('top') <= self.__rect.top: collide_side = 'top'
		elif ball.get_position('left') <= self.__rect.left: collide_side = 'left'
		elif ball.get_position('right') >= self.__rect.right: collide_side = 'right'
		elif ball.get_position('bottom') >= self.__rect.bottom: collide_side = 'bottom'
		
		if collide_side:
			ball.change_direction(collide_side)

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