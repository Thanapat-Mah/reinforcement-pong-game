import pygame
from screen import Screen
from game_panel import GamePanel
from paddle import Paddle
from ball import Ball

def play_game(screen, game_panel, left_paddle, right_paddle, ball):
	run = True
	clock_main = pygame.time.Clock()
	fps = 300	# overall fps limit
	paddle_action_limit = 0
	paddle_action_limit_fps = 30	# fps for paddle movement
	while run:
		clock_main.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		# continuously move the paddle
		keys = pygame.key.get_pressed()
		if paddle_action_limit == 0:
			if keys[pygame.K_UP]:
				right_paddle.up()
				paddle_action_limit = 1
			elif keys[pygame.K_DOWN]:
				right_paddle.down()
				paddle_action_limit = 1

			# temporary make left paddle movable
			if keys[pygame.K_w]:
				left_paddle.up()
				paddle_action_limit = 1
			elif keys[pygame.K_s]:
				left_paddle.down()
				paddle_action_limit = 1

		if paddle_action_limit >= int(fps/paddle_action_limit_fps):
			paddle_action_limit = 0
		elif paddle_action_limit > 0:
			paddle_action_limit += 1

		# update position of ball
		game_panel.check_collision(ball)
		if left_paddle.check_collision(ball):
			ball.change_direction('left')
		if right_paddle.check_collision(ball):
			ball.change_direction('right')
		ball.update_position()

		# drawing component	
		screen.update_screen(game_panel, left_paddle, right_paddle, ball)
	pygame.quit()
	quit()


if __name__ == '__main__':
	pygame.init()
	screen = Screen(fullscreen=False)
	game_panel = GamePanel(grid_enable=True)
	game_panel.set_center(screen.get_center())
	left_paddle_position = game_panel.get_inner_position(side='left')
	left_paddle = Paddle(game_panel.get_rect(), move_size=game_panel.get_block_size())
	left_paddle.set_center(left_paddle_position)
	right_paddle_position = game_panel.get_inner_position(side='right')
	right_paddle = Paddle(game_panel.get_rect(), move_size=game_panel.get_block_size())
	right_paddle.set_center(right_paddle_position)
	ball = Ball(game_panel.get_rect())
	center_panel_position = game_panel.get_inner_position(side='center_block')
	ball.set_center(center_panel_position)

	play_game(screen, game_panel, left_paddle, right_paddle, ball)