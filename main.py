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