import pygame
import random

class Ball:
	def __init__(self, parent_rect, rect=[0, 0, 5, 5], color=(255, 255, 255), move_size=1):
		self.__parent_rect = parent_rect
		self.__rect = pygame.Rect(*rect)
		self.__color = color
		self.__move_size = move_size
		self.__direction = [move_size, move_size]

	### getter --------------------------------------------------------------
	def get_rect(self):
		return self.__rect

	def get_center(self):
		return self.__rect.center
		
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

	def set_move_size(self, new_move_size):
		self.__move_size = new_move_size

	def reset_ball(self, position=False):
		if position:
			self.__rect.center = position
		# else:
		# 	ball_x = random.randint(self.__parent_rect.left, self.__parent_rect.right)
		# 	ball_y = random.randint(self.__parent_rect.top, self.__parent_rect.bottom)
		# 	self.__rect.center = (ball_x, ball_y)
		direction_x = random.choice([self.__move_size, -self.__move_size])
		direction_y = random.choice([self.__move_size, -self.__move_size])
		self.__direction = [direction_x, direction_y]

	def update_position(self):
		self.__rect.topleft = (self.__rect.left+self.__direction[0], self.__rect.top+self.__direction[1])

	def change_direction(self, collide_side):
		if collide_side == 'top': self.__direction[1] = self.__move_size
		elif collide_side == 'left': self.__direction[0] = self.__move_size
		elif collide_side == 'right': self.__direction[0] = -self.__move_size
		elif collide_side == 'bottom': self.__direction[1] = -self.__move_size

	def draw(self, display):
		pygame.draw.rect(display, self.__color, self.__rect)