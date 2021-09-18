"""Minimal gym env
Player can move over the board and collect rewards or fall into holes
"""

import random
import numpy as np
from gym import Env
from gym.spaces import Discrete, Box

class MinimalEnv(Env):

    _EMPTY_FIELD = 0.0
    _FOOD_FIELD = 0.3
    _HOLE_FIELD = 0.5
    _PLAYER_FIELD = 1.0

    def __init__(self, board_size=(5, 10), food_count=3, hole_count=5):

        self.action_space = Discrete(5)
        self.observation_space = Box(0, 1, shape=board_size)
        self.game_board = np.zeros(board_size)

        self.game_board[0][1] = self._PLAYER_FIELD

        # Generate random food
        for _ in range(food_count):
            x = random.randint(0, board_size[0] - 1)
            y = random.randint(0, board_size[1] - 1)
            if self._get_field(x, y) == 0:
                self._set_field(x, y, self._FOOD_FIELD)

        # Generate random holes
        for _ in range(hole_count):
            x = random.randint(0, board_size[0] - 1)
            y = random.randint(0, board_size[1] - 1)
            if self._get_field(x, y) == 0:
                self._set_field(x, y, self._HOLE_FIELD)

        self.render()


    def step(self, action):

        state = 0
        reward = 1
        done = random.randint(1, 100) < 10
        info = {}

        return self.game_board, reward, done, info

    def reset(self):
        return 0

    def render(self, mode='human'):
        print("Board:\n\t" + "\n\t".join(["|" + " ".join([self._number_to_symbol(e) for e in row]) + "|" for row in self.game_board.T]))

    def _check_if_done(self):
        return np.all(self.game_board != self._PLAYER_FIELD)

    def _set_field(self, x, y, value):
        self.game_board[x][y] = value

    def _get_field(self, x, y):
        return self.game_board[x][y]

    def _number_to_symbol(self, number):
        if number == self._EMPTY_FIELD: return " "
        if number == self._PLAYER_FIELD: return "X"
        if number == self._FOOD_FIELD: return "F"
        if number == self._HOLE_FIELD: return "O"

env = MinimalEnv()

for episode in range(1, 2):

    print(f"\n\nEpisode: {episode}")

    obs = env.reset()
    print(f"Initial Observation: {obs}")

    done = False
    while not done:

        random_action = env.action_space.sample()

        obs, reward, done, info = env.step(random_action)
        print(f"{obs=} {reward=} {done=}")

        break
