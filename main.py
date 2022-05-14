import pygame
from screen import Screen
from game_panel import GamePanel
from paddle import Paddle

def play_game(screen, game_panel, paddle):
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			# if event.type == pygame.KEYDOWN:

		# continuously move the paddle
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]: paddle.up()
		elif keys[pygame.K_DOWN]: paddle.down()

		# drawing component	
		screen.update_screen(game_panel, paddle)
	pygame.quit()
	quit()


if __name__ == '__main__':
	pygame.init()
	screen = Screen(fullscreen=False)
	game_panel = GamePanel(grid_enable=False)
	paddle = Paddle()

	play_game(screen, game_panel, paddle)