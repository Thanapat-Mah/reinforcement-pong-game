import pygame

class Ball:
	def __init__(self, parent_rect, rect=[0, 0, 5, 5], color=(255, 255, 255)):
		self.__parent_rect = parent_rect
		self.__rect = pygame.Rect(*rect)
		self.__color = color
		self.__direction = [1, 1]

	### getter --------------------------------------------------------------
	def get_position(self, side='top'):
		if side == 'top': position = self.__rect.top
		elif side == 'left': position = self.__rect.left
		elif side == 'right': position = self.__rect.right
		elif side == 'bottom': position = self.__rect.bottom
		else: position = 0
		return position

	### setter --------------------------------------------------------------
	def set_center(self, center_point):
		self.__rect.center = center_point

	def update_position(self):
		self.__rect.topleft = (self.__rect.left+self.__direction[0], self.__rect.top+self.__direction[1])

	def change_direction(self, collide_side):
		if collide_side == 'top': self.__direction[1] = 1
		elif collide_side == 'left': self.__direction[0] = 1
		elif collide_side == 'right': self.__direction[0] = -1
		elif collide_side == 'bottom': self.__direction[1] = -1

	def draw(self, display):
		pygame.draw.rect(display, self.__color, self.__rect)