import pygame

class GamePanel:
	def __init__(self, panel_size=[800, 500], block_size=[20, 20], background_color=(40, 40, 40), 
		grid_color=(120, 120, 120), grid_enable=True):
		self.__panel_size = panel_size
		self.__block_size = block_size
		self.__block_count = [int(panel_size[0]/block_size[0]), int(panel_size[1]/block_size[1])]
		self.__background_color = background_color
		self.__grid_color = grid_color
		self.__grid_enable = grid_enable

	def draw(self, screen, paddle):
		# draw background
		x = int((screen.get_size()[0] - self.__panel_size[0])/2)
		y = int((screen.get_size()[1] - self.__panel_size[1])/2)
		pygame.draw.rect(screen.get_display(), self.__background_color, (x, y, *self.__panel_size))

		# draw grid
		block_x = x
		block_y = y
		if self.__grid_enable:
			for col in range(self.__block_count[0]):
				for row in range(self.__block_count[1]):
					pygame.draw.rect(screen.get_display(), self.__grid_color, (block_x, block_y, *self.__block_size), 1)
					block_y += self.__block_size[1]
				block_x += self.__block_size[0]
				block_y = y

		# draw paddle
		paddle.draw(screen.get_display(), [x, y], self.__panel_size)