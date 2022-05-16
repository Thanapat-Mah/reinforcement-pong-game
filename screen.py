import pygame

class Screen:
	def __init__(self, size=[1500, 750], fullscreen=False, background_color=(0, 0, 0)):
		self.__fullscreen = fullscreen
		if self.__fullscreen:
			infoObject = pygame.display.Info()
			self.__size = [infoObject.current_w, infoObject.current_h]	# [width, height]
		else:
			self.__size = size
		self.__background_color = background_color
		self.__display = pygame.display.set_mode((self.__size[0], self.__size[1]))
		self.__inner_item = []

	### getter ----------------------------------------------------------------------------------------
	def get_size(self):
		return self.__size

	def get_display(self):
		return self.__display

	def get_center(self):
		return (int(self.__size[0]/2), int(self.__size[1]/2))

	def refresh_background(self):
		self.__display.fill(self.__background_color)

	def update_screen(self, game_panel, left_paddle, ball):
		self.refresh_background()
		game_panel.draw(self.__display)
		left_paddle.draw(self.__display)
		ball.draw(self.__display)
		pygame.display.update()