import pygame
from screen import Screen
from game_panel import GamePanel
from paddle import Paddle
from ball import Ball
from ai import AI
from button import Button
from side_setting import SideSetting

def play_game(screen, game_panel, left_paddle, right_paddle, ball, left_ai, right_ai,
	grid_button, render_button, random_ball_button, fast_button, close_button,
	left_setting, right_setting):
	run = True
	clock_main = pygame.time.Clock()
	high_fps = 10000
	low_fps = 20
	fps = low_fps	# overall fps limit
	paddle_action_count = 0
	paddle_action_limit = 1
	is_fast = False
	is_rendering = True
	left_learn_terminate_count = 0
	left_hit_rate = 0
	left_current_state = game_panel.get_state(ball, left_paddle)
	left_state = left_setting.get_state()
	is_left_learn = left_setting.get_is_learn()
	right_train_terminate_count = 0
	right_hit_rate = 0
	right_current_state = game_panel.get_state(ball, right_paddle)
	right_state = right_setting.get_state()
	is_right_learn = right_setting.get_is_learn()
	while run:
		clock_main.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if grid_button.check_click(event):
				grid_enable = grid_button.get_is_active()
				game_panel.set_grid_enable(grid_enable)
			elif random_ball_button.check_click(event):
				is_random = random_ball_button.get_is_active()
				ball.set_is_respawn_center(not is_random)
			elif fast_button.check_click(event):
				is_fast = fast_button.get_is_active()
				if is_fast:
					fps = high_fps
				else:
					fps = low_fps
			elif render_button.check_click(event):
				is_rendering = render_button.get_is_active()
				if not is_rendering:
					screen.disable_rendering(render_button)
			elif close_button.check_click(event):
				run = False
			elif left_setting.check_click(event, left_ai):
				left_state = left_setting.get_state()
				is_left_learn = left_setting.get_is_learn()
				if left_state != 'Wall':
					game_panel.add_terminal('left')
				else:
					game_panel.remove_terminal('left')
				left_ai.set_values(*left_setting.get_values())
			elif right_setting.check_click(event, right_ai):
				right_state = right_setting.get_state()
				is_right_learn = right_setting.get_is_learn()
				if right_state != 'Wall':
					game_panel.add_terminal('right')
				else:
					game_panel.remove_terminal('right')
				right_ai.set_values(*right_setting.get_values())

		keys = pygame.key.get_pressed()
		if paddle_action_count == 0:
			if left_state == 'AI':
				left_ai.perform_action(left_current_state, best_util_ratio=1)
			elif left_state == 'Player':
				if keys[pygame.K_w]:
					left_paddle.up()
					paddle_action_count = 1
				elif keys[pygame.K_s]:
					left_paddle.down()
					paddle_action_count = 1
			if right_state == 'AI':
				right_ai.perform_action(right_current_state, best_util_ratio=1)
			elif right_state == 'Player':
				if keys[pygame.K_UP]:
					right_paddle.up()
					paddle_action_count = 1
				elif keys[pygame.K_DOWN]:
					right_paddle.down()
					paddle_action_count = 1
			paddle_action_count = 1

		# limit the speed of paddle
		if paddle_action_count >= paddle_action_limit:
			paddle_action_count = 0
		elif paddle_action_count > 0:
			paddle_action_count += 1

		# update position of ball
		panel_collide_side = game_panel.check_collision(ball)
		if left_state != 'Wall':
			left_paddle_collide = left_paddle.check_collision(ball)
			if left_paddle_collide:
				ball.change_direction('left')
			left_new_state = game_panel.get_state(ball, left_paddle)
			left_current_state = left_new_state
		if right_state != 'Wall':
			right_paddle_collide = right_paddle.check_collision(ball)
			if right_paddle_collide:
				ball.change_direction('right')
			right_new_state = game_panel.get_state(ball, right_paddle)
			right_current_state = right_new_state
		ball.update_position()

		# learning from the previous action
		# when learning AI reach 100% hit rate, force enable rendering and close fast simulate
		if (left_state == 'AI') and is_left_learn:
			left_ball_position_in_danger = ball.get_rect().left < left_paddle.get_left()
			left_ai.learn(panel_collide_side, left_paddle_collide, left_new_state, left_ball_position_in_danger)
			if left_ai.get_first_converge():
				render_button.set_is_active(True)
				is_rendering = True
				fast_button.set_is_active(False)
				is_fast = False
				fps = low_fps
				left_ai.reset_first_converge()
		left_learn_terminate_count = left_ai.get_learn_count()
		left_hit_rate = left_ai.get_hit_rate()
		if (right_state == 'AI') and is_right_learn:
			right_ball_position_in_danger = ball.get_rect().right > right_paddle.get_right()
			right_ai.learn(panel_collide_side, right_paddle_collide, right_new_state, right_ball_position_in_danger)
			if right_ai.get_first_converge():
				render_button.set_is_active(True)
				is_rendering = True
				fast_button.set_is_active(False)
				is_fast = False
				fps = low_fps
				right_ai.reset_first_converge()
		right_train_terminate_count = right_ai.get_learn_count()
		right_hit_rate = right_ai.get_hit_rate()
		if is_rendering:
			screen.update_screen(game_panel, left_paddle, right_paddle, ball,
				grid_button, render_button, random_ball_button, fast_button,
				is_fast, left_learn_terminate_count, right_train_terminate_count, close_button,
				left_setting, right_setting, left_hit_rate, right_hit_rate)

	pygame.quit()
	quit()


if __name__ == '__main__':
	pygame.init()

	screen = Screen(fullscreen=True)

	game_panel = GamePanel(grid_enable=True)
	game_panel.set_center(screen.get_center())

	left_paddle = Paddle(game_panel.get_rect(), rect=[0, 0, 5, 100], move_size=game_panel.get_block_size())
	left_paddle.set_center(game_panel.get_inner_position(side='left'))

	right_paddle = Paddle(game_panel.get_rect(), rect=[0, 0, 5, 100], move_size=game_panel.get_block_size())
	right_paddle.set_center(game_panel.get_inner_position(side='right'))

	ball = Ball(game_panel.get_rect(), move_size=game_panel.get_block_size())
	ball.reset_ball(game_panel.get_inner_position(side='center'))

	left_ai = AI(left_paddle, 'left')
	right_ai = AI(right_paddle, 'right')

	grid_button = Button(text='Enable grid', active_color=(100, 100, 200))
	grid_button.set_midtop(game_panel.get_inner_position(side='grid_button'))

	render_button = Button(text='Enable rendering', active_color=(100, 100, 200))
	render_button.set_topleft(game_panel.get_inner_position(side='render_button'))

	random_ball_button = Button(text='Random spawn ball', active_color=(100, 100, 200))
	random_ball_button.set_topright(game_panel.get_inner_position(side='random_ball_button'))

	fast_button = Button(text='Fast simulate', active_color=(100, 200, 100))
	fast_button.set_is_active(False)
	fast_button.set_midbottom(game_panel.get_inner_position(side='fast_button'))

	close_button = Button(text='Close program', active_color=(200, 100, 100), passive_color=(200, 100, 100))
	close_button.set_topright((screen.get_size()[0]-20, 20))

	left_setting = SideSetting()
	left_setting.set_midright(game_panel.get_inner_position(side='left_setting'))

	right_setting = SideSetting(state='Wall')
	right_setting.set_midleft(game_panel.get_inner_position(side='right_setting'))


	play_game(screen, game_panel, left_paddle, right_paddle, ball, left_ai, right_ai, 
		grid_button, render_button, random_ball_button, fast_button, close_button,
		left_setting, right_setting)

# q_table = {
# 	'state1': {'up': 10, 'down': -10, 'stay': 0},
# 	'state2': {'up': 10, 'down': -10, 'stay': 0}
# }