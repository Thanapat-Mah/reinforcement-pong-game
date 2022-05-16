import pygame
from screen import Screen
from game_panel import GamePanel
from paddle import Paddle
from ball import Ball
from ai import AI

def play_game(screen, game_panel, left_paddle, ball):
	run = True
	clock_main = pygame.time.Clock()
	fps = 30	# overall fps limit
	paddle_action_count = 0
	paddle_action_limit = 10
	while run:
		clock_main.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		# continuously move the paddle
		keys = pygame.key.get_pressed()
		if paddle_action_count == 0:
			# temporary make left paddle movable
			if keys[pygame.K_w]:
				left_paddle.up()
				paddle_action_count = 1
			elif keys[pygame.K_s]:
				left_paddle.down()
				paddle_action_count = 1

		if paddle_action_count >= paddle_action_limit:
			paddle_action_count = 0
		elif paddle_action_count > 0:
			paddle_action_count += 1

		# update position of ball
		game_panel.check_collision(ball)
		if left_paddle.check_collision(ball):
			ball.change_direction('left')
		ball.update_position()

		# drawing component
		screen.update_screen(game_panel, left_paddle, ball)
		game_panel.get_state(ball, left_paddle)
	pygame.quit()
	quit()


if __name__ == '__main__':
	pygame.init()

	screen = Screen(fullscreen=False)

	game_panel = GamePanel(grid_enable=False)
	game_panel.set_center(screen.get_center())

	left_paddle = Paddle(game_panel.get_rect(), move_size=game_panel.get_block_size())
	left_paddle.set_center(game_panel.get_inner_position(side='left'))

	ball = Ball(game_panel.get_rect(), move_size=1)
	ball.set_center(game_panel.get_inner_position(side='center'))

	left_ai = AI(left_paddle, game_panel.get_state(ball, left_paddle))

	play_game(screen, game_panel, left_paddle, ball)

# q_table = {
# 	'state1': {'up': 10, 'down': -10, 'stay': 0},
# 	'state2': {'up': 10, 'down': -10, 'stay': 0}
# }