import pygame

class GamePanel:
	def __init__(self, rect=[0, 0, 800, 500], block_size=20, background_color=(40, 40, 40), 
		grid_color=(120, 120, 120), grid_enable=True):
		self.__rect = pygame.Rect(*rect)
		self.__block_size = block_size
		self.__block_count = [int(rect[2]/block_size), int(rect[3]/block_size)]
		self.__background_color = background_color
		self.__grid_color = grid_color
		self.__grid_enable = grid_enable

	### setter --------------------------------------------------------------------------------
	def set_center(self, center_point):
		self.__rect.center = center_point

	### getter --------------------------------------------------------------------------------
	def get_rect(self):
		return self.__rect

	def get_block_size(self):
		return self.__block_size

	def get_paddle_inner_position(self, side):
		if side == 'left':
			position = (self.__block_size, self.__rect.centery-self.__rect.top)
		elif side == 'right':
			position = (self.__rect.right-self.__block_size, self.__rect.centery - self.__rect.top)
		else:
			position = self.__rect.center
		return position

	def draw(self, screen):
		# draw background
		pygame.draw.rect(screen.get_display(), self.__background_color, self.__rect)

		# draw grid
		block_x = self.__rect.left
		block_y = self.__rect.top
		if self.__grid_enable:
			for col in range(self.__block_count[0]):
				for row in range(self.__block_count[1]):
					pygame.draw.rect(screen.get_display(), self.__grid_color,
						(block_x, block_y, self.__block_size, self.__block_size), 1)
					block_y += self.__block_size
				block_x += self.__block_size
				block_y = self.__rect.top