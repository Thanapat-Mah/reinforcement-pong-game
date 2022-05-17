import pygame
from button import Button
from value_adjustor import ValueAdjustor

class SideSetting:
	def __init__(self, rect=[0, 0, 200, 400], border_radius=20, background_color=(40, 40, 40), state='AI'):
		self.__rect = pygame.Rect(rect)
		self.__border_radius = border_radius
		self.__background_color = background_color
		self.__buttons = {
			'Wall': Button(text='Wall', rect=[0, 0, 150, 40], active_color=(180, 100, 200)),
			'AI': Button(text='AI', rect=[0, 0, 150, 40], active_color=(180, 100, 200)),
			'Player': Button(text='Player', rect=[0, 0, 150, 40], active_color=(180, 100, 200))
		}
		self.__value_adjustors = {
			'Alpha': ValueAdjustor(value_label='α', rect=[0, 0, 150, 30]),
			'Gamma': ValueAdjustor(value_label='γ', rect=[0, 0, 150, 30]),
		}
		self.__ai_setting = {
			'Learn': Button(text='Learn', rect=[0, 0, 150, 40], active_color=(100, 200, 100)),
			'Reset': Button(text='Reset', text_color=(255, 100, 100), rect=[0, 0, 150, 40],
				active_color=(100, 100, 100), passive_color=(100, 100, 100))
		}
		self.__ai_setting['Learn'].set_is_active(False)
		self.__state = state
		self.adjust_elements()
		self.justify_state()

	### getter ------------------------------------------------------------------
	def get_state(self):
		return self.__state

	def get_is_learn(self):
		return self.__ai_setting['Learn'].get_is_active()

	def get_values(self):
		return self.__value_adjustors['Alpha'].get_value(), self.__value_adjustors['Gamma'].get_value()

	### setter ------------------------------------------------------------------
	def set_midleft(self, midleft):
		self.__rect.midleft = midleft
		self.adjust_elements()

	def set_midright(self, midright):
		self.__rect.midright = midright
		self.adjust_elements()

	def set_values(self, alpha, gamma):
		self.__value_adjustors['Alpha'] = alpha
		self.__value_adjustors['Gamma'] = gamma

	def adjust_elements(self):
		button_x = self.__rect.left + int((self.__rect.width-150)/2)
		button_y = self.__rect.top + 30
		for data, button in self.__buttons.items():
			button.set_topleft((button_x, button_y))
			button_y += 50
		button_y += 10
		for value_label, value_adjustor in self.__value_adjustors.items():
			value_adjustor.set_topleft((button_x, button_y))
			button_y += 40
		button_y += 10
		for setting, button in self.__ai_setting.items():
			button.set_topleft((button_x, button_y))
			button_y += 50

	def justify_state(self):
		for data, button in self.__buttons.items():
			if data != self.__state:
				button.set_is_active(False)
			else:
				button.set_is_active(True)

	def check_click(self, event, ai):
		for data, button in self.__buttons.items():
			if button.check_click(event):
				self.__state = data
				self.justify_state()
				return self.__state
		if self.__state == 'AI':
			if self.__ai_setting['Learn'].check_click(event):
				return 'Learn'
			if self.__ai_setting['Reset'].check_click(event):
				ai.reset()
				return 'Reset'
			for value_label, value_adjustor in self.__value_adjustors.items():
				if value_adjustor.check_click(event):
					return True


	def draw(self, display):
		pygame.draw.rect(display, self.__background_color, self.__rect, border_radius=self.__border_radius)
		for data, button in self.__buttons.items():
			button.draw(display)
		if self.__state == 'AI':
			for setting, button in self.__ai_setting.items():
				button.draw(display)
			for value_label, value_adjustor in self.__value_adjustors.items():
				value_adjustor.draw(display)
