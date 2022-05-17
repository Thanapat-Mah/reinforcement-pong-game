import pygame
from screen import Screen
from game_panel import GamePanel
from paddle import Paddle
from ball import Ball
from ai import AI
from button import Button
from side_setting import SideSetting

def play_game(screen, game_panel, left_paddle, right_paddle, ball, left_ai, right_ai,
	grid_button, render_button, train_button,
	left_setting, right_setting):
	run = True
	clock_main = pygame.time.Clock()
	fps = 10	# overall fps limit
	paddle_action_count = 0
	paddle_action_limit = 1
	left_train_terminate_count = 0
	right_train_terminate_count = 0
	left_current_state = game_panel.get_state(ball, left_paddle)
	right_current_state = game_panel.get_state(ball, right_paddle)
	is_train = False
	is_rendering = True
	while run:
		clock_main.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if grid_button.check_click(event):
				grid_enable = grid_button.get_is_active()
				game_panel.set_grid_enable(grid_enable)
			elif train_button.check_click(event):
				is_train = not train_button.get_is_active()
				if is_train:
					fps = 10000
				else:
					fps = 30
			elif render_button.check_click(event):
				is_rendering = render_button.get_is_active()
				if not is_rendering:
					screen.disable_rendering(render_button)
			elif left_setting.check_click(event):
				pass
			elif right_setting.check_click(event):
				pass

		keys = pygame.key.get_pressed()
		if paddle_action_count == 0:
			left_ai.perform_action(left_current_state, best_util_ratio=1)
			right_ai.perform_action(right_current_state, best_util_ratio=1)
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
		right_paddle_collide = right_paddle.check_collision(ball)
		if left_paddle_collide:
			ball.change_direction('left')
		elif right_paddle_collide:
			ball.change_direction('right')
		ball.update_position()
		left_new_state = game_panel.get_state(ball, left_paddle)
		left_current_state = left_new_state
		right_new_state = game_panel.get_state(ball, right_paddle)
		right_current_state = right_new_state

		# learning from the previous action
		if is_train:
			left_ball_position_in_danger = ball.get_rect().left < left_paddle.get_left()
			left_train_terminate_count = left_ai.learn(panel_collide_side, left_paddle_collide, left_new_state, left_ball_position_in_danger)
			right_ball_position_in_danger = ball.get_rect().right > right_paddle.get_right()
			right_train_terminate_count = right_ai.learn(panel_collide_side, right_paddle_collide, right_new_state, right_ball_position_in_danger)
		if is_rendering:
			screen.update_screen(game_panel, left_paddle, right_paddle, ball, grid_button, render_button, train_button, 
				is_train, left_train_terminate_count, right_train_terminate_count, left_setting, right_setting)

		# if (count%100000 == 0) and (count != 0): left_ai.get_states()
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
	right_ai = AI(right_paddle, 'right', game_panel.get_state(ball, right_paddle))

	grid_button = Button(text='Enable grid', active_color=(100, 100, 200))
	grid_button.set_midtop(game_panel.get_inner_position(side='grid_button'))

	render_button = Button(text='Enable rendering', active_color=(100, 100, 200))
	render_button.set_topleft(game_panel.get_inner_position(side='render_button'))

	train_button = Button(text='Train', active_color=(100, 200, 100))
	train_button.set_midbottom(game_panel.get_inner_position(side='train_button'))

	left_setting = SideSetting()
	left_setting.set_midright(game_panel.get_inner_position(side='left_setting'))

	right_setting = SideSetting(state='Wall')
	right_setting.set_midleft(game_panel.get_inner_position(side='right_setting'))


	play_game(screen, game_panel, left_paddle, right_paddle, ball, left_ai, right_ai, 
		grid_button, render_button, train_button,
		left_setting, right_setting)

# q_table = {
# 	'state1': {'up': 10, 'down': -10, 'stay': 0},
# 	'state2': {'up': 10, 'down': -10, 'stay': 0}
# }