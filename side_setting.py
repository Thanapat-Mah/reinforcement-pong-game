import pygame
from button import Button

class SideSetting:
	def __init__(self, rect=[0, 0, 200, 400], border_radius=20, background_color=(40, 40, 40), state='AI'):
		self.__rect = pygame.Rect(rect)
		self.__border_radius = border_radius
		self.__background_color = background_color
		self.__buttons = {
			'Wall': Button(text='Wall', rect=[0, 0, 150, 50], active_color=(180, 100, 200)),
			'AI': Button(text='AI', rect=[0, 0, 150, 50], active_color=(180, 100, 200)),
			'Player': Button(text='Player', rect=[0, 0, 150, 50], active_color=(180, 100, 200))
		}
		self.__state = state
		self.adjust_buttons()
		self.justify_state()

	### getter ------------------------------------------------------------------
	def get_state(self):
		return self.__state

	### setter ------------------------------------------------------------------
	def set_midleft(self, midleft):
		self.__rect.midleft = midleft
		self.adjust_buttons()

	def set_midright(self, midright):
		self.__rect.midright = midright
		self.adjust_buttons()


	def adjust_buttons(self):
		button_x = self.__rect.left + int((self.__rect.width-150)/2)
		button_y = self.__rect.top + 30
		for data, button in self.__buttons.items():
			button.set_topleft((button_x, button_y))
			button_y += 60

	def justify_state(self):
		for data, button in self.__buttons.items():
			if data != self.__state:
				button.set_is_active(False)
			else:
				button.set_is_active(True)

	def check_click(self, event):
		for data, button in self.__buttons.items():
			if button.check_click(event):
				self.__state = data
				self.justify_state()
				return self.__state

	def draw(self, display):
		pygame.draw.rect(display, self.__background_color, self.__rect, border_radius=self.__border_radius)
		for data, button in self.__buttons.items():
			button.draw(display)