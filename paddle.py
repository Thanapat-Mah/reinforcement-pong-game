import pygame

class Paddle:
	def __init__(self, position=[0, 0], size=[5, 60], color=(255, 255, 255), move_size=20):
		self.__position = position
		self.__size = size
		self.__color = color
		self.__move_size = move_size

	def up(self):
		self.__position = [self.__position[0], self.__position[1] + self.__move_size]

	def down(self):
		self.__position = [self.__position[0], self.__position[1] - self.__move_size]

	def draw(self, display, parent_position):
		x = self.__position[0] + parent_position[0]
		y = self.__position[1] + parent_position[1]
		pygame.draw.rect(display, self.__color, (x, y, *self.__size))