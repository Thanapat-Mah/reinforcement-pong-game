import pygame
from screen import Screen
from game_panel import GamePanel
from paddle import Paddle
from ball import Ball
from ai import AI
from button import Button

def play_game(screen, game_panel, left_paddle, ball, left_ai, grid_button):
	run = True
	clock_main = pygame.time.Clock()
	fps = 30000000000	# overall fps limit
	paddle_action_count = 0
	paddle_action_limit = 1
	count = 0
	current_state = game_panel.get_state(ball, left_paddle)
	while run:
		clock_main.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if grid_button.check_click(event):
				grid_enable = grid_button.get_is_active()
				game_panel.set_grid_enable(grid_enable)

		# continuously move the paddle
		keys = pygame.key.get_pressed()
		if paddle_action_count == 0:			
			left_ai.perform_action(current_state, best_util_ratio=1)
			paddle_action_count = 1
			### temporary make right paddle movable
			# if keys[pygame.K_UP]:
			# 	right_paddle.up()
			# 	paddle_action_count = 1
			# elif keys[pygame.K_DOWN]:
			# 	right_paddle.down()
			# 	paddle_action_count = 1

		# limit the speed of paddle
		if paddle_action_count >= paddle_action_limit:
			paddle_action_count = 0
		elif paddle_action_count > 0:
			paddle_action_count += 1

		# update position of ball
		panel_collide_side = game_panel.check_collision(ball)
		left_paddle_collide = left_paddle.check_collision(ball)
		if left_paddle_collide:
			ball.change_direction('left')
		ball.update_position()

		# learning from the previous action
		new_state = game_panel.get_state(ball, left_paddle)
		left_ball_position_in_danger = ball.get_rect().left < left_paddle.get_left()
		left_ai.learn(panel_collide_side, left_paddle_collide, new_state, left_ball_position_in_danger)
		current_state = new_state

		if count > 1000000:
			fps = 10
			screen.update_screen(game_panel, left_paddle, ball, grid_button)

		# if (count%100000 == 0) and (count != 0): left_ai.get_states()
		count += 1
	pygame.quit()
	quit()


if __name__ == '__main__':
	pygame.init()

	screen = Screen(fullscreen=False)

	game_panel = GamePanel(grid_enable=True)
	game_panel.set_center(screen.get_center())

	left_paddle = Paddle(game_panel.get_rect(), rect=[0, 0, 5, 100], move_size=game_panel.get_block_size())
	left_paddle.set_center(game_panel.get_inner_position(side='left'))

	right_paddle = Paddle(game_panel.get_rect(), rect=[0, 0, 5, 100], move_size=game_panel.get_block_size())
	right_paddle.set_center(game_panel.get_inner_position(side='right'))

	ball = Ball(game_panel.get_rect(), move_size=game_panel.get_block_size())
	ball.reset_ball(game_panel.get_inner_position(side='center'))

	left_ai = AI(left_paddle, 'left', game_panel.get_state(ball, left_paddle))

	grid_button = Button(text='Enable grid')
	grid_button.set_midtop(game_panel.get_inner_position(side='grid_button'))

	play_game(screen, game_panel, left_paddle, ball, left_ai, grid_button)

# q_table = {
# 	'state1': {'up': 10, 'down': -10, 'stay': 0},
# 	'state2': {'up': 10, 'down': -10, 'stay': 0}
# }