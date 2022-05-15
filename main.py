import pygame
from screen import Screen
from game_panel import GamePanel
from paddle import Paddle

def play_game(screen, game_panel, left_paddle):
	run = True
	while run:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			# if event.type == pygame.KEYDOWN:

		# continuously move the paddle
		keys = pygame.key.get_pressed()
		if keys[pygame.K_UP]: left_paddle.up()
		elif keys[pygame.K_DOWN]: left_paddle.down()

		# drawing component	
		screen.update_screen(game_panel, left_paddle)
	pygame.quit()
	quit()


if __name__ == '__main__':
	pygame.init()
	screen = Screen(fullscreen=False)
	game_panel = GamePanel(grid_enable=True)
	game_panel.set_center(screen.get_center())
	left_paddle_position = game_panel.get_paddle_inner_position(side='left')
	left_paddle = Paddle(game_panel.get_rect(), move_size=game_panel.get_block_size())
	left_paddle.set_center(left_paddle_position)

	play_game(screen, game_panel, left_paddle)