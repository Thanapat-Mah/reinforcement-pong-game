import pygame
from screen import Screen
from game_panel import GamePanel
from paddle import Paddle
from ball import Ball
from ai import AI

def play_game(screen, game_panel, left_paddle, ball, left_ai):
	run = True
	clock_main = pygame.time.Clock()
	fps = 30000000	# overall fps limit
	paddle_action_count = 0
	paddle_action_limit = 1
	count = 0
	current_state = game_panel.get_state(ball, left_paddle)
	while run:
		clock_main.tick(fps)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

		# continuously move the paddle
		keys = pygame.key.get_pressed()
		if paddle_action_count == 0:			
			action_reward = left_ai.perform_action(current_state, best_util_ratio=1)
			paddle_action_count = 1

			# ### temporary make left paddle movable
			# if keys[pygame.K_w]:
			# 	left_paddle.up()
			# 	paddle_action_count = 1
			# elif keys[pygame.K_s]:
			# 	left_paddle.down()
			# 	paddle_action_count = 1

		if paddle_action_count >= paddle_action_limit:
			paddle_action_count = 0
		elif paddle_action_count > 0:
			paddle_action_count += 1

		# update position of ball
		panel_collide_side = game_panel.check_collision(ball)
		paddle_collide = left_paddle.check_collision(ball)
		if paddle_collide:
			ball.change_direction('left')
		ball.update_position()

		# learning from the previous action
		state_utility = 0
		if panel_collide_side == 'left':
			state_utility = -1
		elif paddle_collide:
			state_utility = 1
		elif ball.get_rect().left < left_paddle.get_left():
			state_utility = -0.5
		new_state = game_panel.get_state(ball, left_paddle)
		left_ai.learn(action_reward, state_utility, new_state)
		current_state = new_state

		if count > 1000000:
			fps = 10
			screen.update_screen(game_panel, left_paddle, ball)

		count += 1
	pygame.quit()
	quit()


if __name__ == '__main__':
	pygame.init()

	screen = Screen(fullscreen=False)

	game_panel = GamePanel(grid_enable=False)
	game_panel.set_center(screen.get_center())

	left_paddle = Paddle(game_panel.get_rect(), rect=[0, 0, 5, 100], move_size=game_panel.get_block_size())
	left_paddle.set_center(game_panel.get_inner_position(side='left'))

	ball = Ball(game_panel.get_rect(), move_size=game_panel.get_block_size())
	ball.reset_ball(game_panel.get_inner_position(side='center'))

	left_ai = AI(left_paddle, game_panel.get_state(ball, left_paddle))

	play_game(screen, game_panel, left_paddle, ball, left_ai)

# q_table = {
# 	'state1': {'up': 10, 'down': -10, 'stay': 0},
# 	'state2': {'up': 10, 'down': -10, 'stay': 0}
# }