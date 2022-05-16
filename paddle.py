import pygame

class Paddle:
	def __init__(self, parent_rect, rect=[0, 0, 5, 60], color=(255, 255, 255), move_size=1):
		self.__parent_rect = parent_rect
		self.__rect = pygame.Rect(*rect)
		self.__color = color
		self.__move_size = move_size

	def get_center(self):
		return self.__rect.center

	def get_left(self):
		return self.__rect.left

	### setter ----------------------------------------------------------------------------------
	def set_center(self, center_point):
		self.__rect.center = center_point

	def up(self):
		self.__rect.top -= self.__move_size
		self.justity_position()

	def down(self):
		self.__rect.top += self.__move_size
		self.justity_position()

	def perform(self, action):
		if action == 'up':
			self.up()
		elif action == 'down':
			self.down()

	def justity_position(self):
		# make the paddle don't go out the parent area
		if self.__rect.top <= self.__parent_rect.top:
			self.__rect.top = self.__parent_rect.top
		elif self.__rect.bottom >= self.__parent_rect.bottom:
			self.__rect.bottom = self.__parent_rect.bottom

	def check_collision(self, ball):
		return self.__rect.colliderect(ball.get_rect())

	def draw(self, display):
		pygame.draw.rect(display, self.__color, self.__rect)