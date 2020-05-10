import math
import os

import numpy as np
import pygame

from PyPong import PyPong, Ball, Paddle
from agent import Agent

if __name__ == '__main__':
    width = 700
    height = 400
    black = (0, 0, 0)
    white = (255, 255, 255)
    blue = (0, 0, 255)
    red = (255, 0, 0)

    print(os.getcwd())
    size = [width, height]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("PyPong")

    # Loop until the user clicks the close button.
    done = False
    clock = pygame.time.Clock()

    ball = Ball(width / 2, height / 2, 0, height, width)

    player1 = Paddle(height / 3, 40, height / 6, red, height, width)
    player2 = Paddle(height / 3, width - 50, height / 6, blue, height, width)

    game = PyPong(screen, ball, player1, player2, width, height)
    pygame.init()

    agent = Agent(load_weights=True)

    action = 0
    player1_pos, ball_pos_x, ball_pos_y, ball_velocity, ball_direction, score1, score2 = game.step(action)

    game_state = np.array([player1_pos/height, ball_pos_x/width, ball_pos_y/height, ball_velocity/10, ball_direction/360]).reshape(1, 5)

    i = 0
    prev_score = -1
    reward = 0
    memory = []
    steps_taken = 0

    while True:
        clock.tick(45)

        action = agent.get_prediction(game_state)

        player1_pos, ball_pos_x, ball_pos_y, ball_velocity, ball_direction, score1, score2 = game.step(action)

        returned_score = score1 - score2

        game_state_new = np.array(
            [player1_pos / height, ball_pos_x / width, ball_pos_y / height, ball_velocity / 10, ball_direction/360]).reshape(1, 5)

        if prev_score != returned_score:

            if returned_score > prev_score:
                reward = 1
            elif prev_score > returned_score:
                reward = -1

            for item in memory:
                if returned_score > prev_score:
                    reward = 1
                elif prev_score > returned_score:
                    reward = -1

                reward+=item[2] * 1e-3
                reward-=math.log(abs(item[0][0][2] * height - item[0][0][0] * height)) * 1e-4

                print("Reward: ", reward)

                agent.get_sample((item[0], item[1], reward, item[3]))

            agent.backward()
            steps_taken = 0
        else:
            steps_taken += 1
            memory.append((game_state, action, steps_taken, game_state_new))

        i = i+ 1

        game_state = game_state_new

        agent.save_model_weights()
        prev_score = returned_score