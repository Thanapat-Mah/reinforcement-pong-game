import pygame

class Paddle:
	def __init__(self, parent_rect, rect=[0, 0, 5, 60], color=(255, 255, 255), move_size=20):
		self.__parent_rect = parent_rect
		self.__rect = pygame.Rect(*rect)
		self.__color = color
		self.__move_size = move_size

	### setter ----------------------------------------------------------------------------------
	def set_center(self, center_point):
		self.__rect.center = center_point

	def up(self):
		self.__rect.top -= self.__move_size
		self.justity_position()

	def down(self):
		self.__rect.top += self.__move_size
		self.justity_position()

	def justity_position(self):
		# make the paddle don't go out the parent area
		if self.__rect.top < 0:
			self.__rect.top = 0
		elif self.__rect.bottom > (self.__parent_rect.bottom-self.__parent_rect.top):
			self.__rect.bottom = (self.__parent_rect.bottom-self.__parent_rect.top)

	def draw(self, display):
		x = self.__rect.left+self.__parent_rect.left
		y = self.__rect.top+self.__parent_rect.top
		pygame.draw.rect(display, self.__color,(x, y, *self.__rect.size))