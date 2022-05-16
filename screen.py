import pygame

pygame.font.init()
font_consola = pygame.font.Font('./CONSOLA.TTF', 18)

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

	def disable_rendering(self, render_button):
		self.refresh_background()
		render_button.draw(self.__display)
		pygame.display.update()

	def update_screen(self, game_panel, left_paddle, ball, grid_button, render_button, train_button, is_train, trian_terminate_count):
		self.refresh_background()
		
		if render_button.get_is_active():
			game_panel.draw(self.__display)
			left_paddle.draw(self.__display)
			ball.draw(self.__display)
			grid_button.draw(self.__display)
			train_button.draw(self.__display)
			render_button.draw(self.__display)

			# display trian terminate count when in training
			text_surface = font_consola.render(f'Trian count: {trian_terminate_count}', True, (255, 255, 255))
			topleft_panel = game_panel.get_rect().topleft
			padding_x = 10
			padding_y = text_surface.get_size()[1] + 20
			self.__display.blit(text_surface, (topleft_panel[0]+padding_x, topleft_panel[1]-padding_y))

		pygame.display.update()