import pygame
from button import Button

pygame.font.init()
font_consola = pygame.font.Font('./CONSOLA.TTF', 16)

class ValueAdjustor:
	def __init__(self, rect=[0, 0, 150, 30], background_color=(60, 60, 60), border_radius=5,
		font=font_consola, label_color=(255, 255, 255), value_label='Value: ',
		value=0.8, max_value=1, min_value=0.05, change_step=0.05):
		self.__rect = pygame.Rect(*rect)
		self.__background_color = background_color
		self.__label_color = label_color
		self.__border_radius = border_radius
		self.__font = font_consola
		self.__value_label = value_label
		self.__value = value
		self.__max_value = max_value
		self.__min_value = min_value
		self.__change_step = change_step
		self.__decrease_button = Button(text='-', rect=[0, 0, 30, 30], active_color=(200, 100, 100), passive_color=(200, 100, 100))
		self.__increase_button = Button(text='+', rect=[0, 0, 30, 30], active_color=(100, 200, 100), passive_color=(100, 200, 100))
		self.adjust_buttons()

	### getter --------------------------------------------------------------
	def get_value(self):
		return self.__value

	## setter ---------------------------------------------------------------
	def set_value(self, new_value):
		self.__value = new_value

	def set_topleft(self, topleft):
		self.__rect.topleft = topleft
		self.adjust_buttons()

	def adjust_buttons(self):
		self.__decrease_button.set_topleft(self.__rect.topleft)
		self.__increase_button.set_topright(self.__rect.topright)

	def check_click(self, event):
		clicked = False
		if self.__decrease_button.check_click(event):
			self.__value -= self.__change_step
			clicked = True
		elif self.__increase_button.check_click(event):
			self.__value += self.__change_step
			clicked = True
		if self.__value < self.__min_value:
			self.__value = self.__min_value
		elif self.__value > self.__max_value:
			self.__value = self.__max_value
		return clicked

	def draw(self, display):
		pygame.draw.rect(display, self.__background_color, self.__rect, width=0, border_radius=self.__border_radius)

		text_surface = self.__font.render(f'{self.__value_label} = {self.__value:1.2f}', True, self.__label_color)
		text_x = self.__rect.left + int((self.__rect.width-text_surface.get_size()[0])/2)
		text_y = self.__rect.top + int((self.__rect.height-text_surface.get_size()[1])/2)
		display.blit(text_surface, (text_x, text_y))

		self.__decrease_button.draw(display)
		self.__increase_button.draw(display)