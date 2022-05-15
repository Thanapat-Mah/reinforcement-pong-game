import pygame

class Ball:
	def __init__(self, parent_rect, rect=[0, 0, 5, 5], color=(255, 255, 255)):
		self.__parent_rect = parent_rect
		self.__rect = pygame.Rect(*rect)
		self.__color = color

	### setter --------------------------------------------------------------
	def set_center(self, center_point):
		self.__rect.center = center_point

	def draw(self, display):
		x = self.__rect.left+self.__parent_rect.left
		y = self.__rect.top+self.__parent_rect.top
		pygame.draw.rect(display, self.__color,(x, y, *self.__rect.size))