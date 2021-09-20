"""Minimal gym env
Player can move over the board and collect rewards or fall into holes
"""

import random
import sys
from typing import Tuple
import numpy as np
from gym import Env
from gym.spaces import Discrete, Box
from stable_baselines3 import PPO
import directions

class MinimalEnv(Env):

    _EMPTY_FIELD = 0.0
    _FOOD_FIELD = 0.3
    _HOLE_FIELD = 0.5
    _PLAYER_FIELD = 1.0

    def __init__(self, board_size=(5, 10), food_count=3, hole_count=5):

        self.action_space = Discrete(4)
        self.observation_space = Box(0, 1, shape=board_size)

        self.board_size = board_size
        self.food_count = food_count
        self.hole_count = hole_count

    def step(self, action):

        assert action in range(4)

        direction = None
        if action == 0: direction = directions.Direction.UP
        if action == 1: direction = directions.Direction.LEFT
        if action == 2: direction = directions.Direction.DOWN
        if action == 3: direction = directions.Direction.RIGHT

        reward, done = self._move_player(direction)
        info = {}

        return self.game_board, reward, done, info

    def reset(self):
        self.game_board = np.zeros(self.board_size)

        self._set_field(0, 0, self._PLAYER_FIELD)

        # Generate random food
        for _ in range(self.food_count):
            x = random.randint(0, self.board_size[0] - 1)
            y = random.randint(0, self.board_size[1] - 1)
            if self._get_field(x, y) == 0:
                self._set_field(x, y, self._FOOD_FIELD)

        # Generate random holes
        for _ in range(self.hole_count):
            x = random.randint(0, self.board_size[0] - 1)
            y = random.randint(0, self.board_size[1] - 1)
            if self._get_field(x, y) == 0:
                self._set_field(x, y, self._HOLE_FIELD)

        return self.game_board

    def render(self, mode='human'):
        print(f"Board: {self._get_player_position()}")
        print("\t" + "\n\t".join(["|" + " ".join([self._number_to_symbol(e) for e in row]) + "|" for row in self.game_board.T]))

    def _move_player(self, direction: directions.Direction) -> Tuple[int, bool]:
        """Moves the player, returns true if the player died"""

        old_pos = self._get_player_position()

        # Getting the new position of the player
        current_pos = [old_pos[0], old_pos[1]]
        if direction == directions.Direction.UP: current_pos[1] -= 1
        if direction == directions.Direction.LEFT: current_pos[0] -= 1
        if direction == directions.Direction.DOWN: current_pos[1] += 1
        if direction == directions.Direction.RIGHT: current_pos[0] += 1

        # Testing if the player moved out of bounds
        if current_pos[0] < 0: return (0, True)
        if current_pos[0] > self.game_board.shape[0] - 1: return (0, True)
        if current_pos[1] < 0: return (0, True)
        if current_pos[1] > self.game_board.shape[1] - 1: return (0, True)

        # Storing original value of the field
        field_value = self._get_field(current_pos[0], current_pos[1])

        # Moving the player to the new field
        self._set_field(old_pos[0], old_pos[1], self._EMPTY_FIELD)
        self._set_field(current_pos[0], current_pos[1], self._PLAYER_FIELD)

        # Checking if we landed on food or a hole
        if field_value == self._FOOD_FIELD: return (1, False)
        if field_value == self._HOLE_FIELD: return (0, True)

        # Extra reward if the player found all food
        if self._check_if_done():
            return (10, True)

        return (0, False)

    def _get_player_position(self) -> Tuple[int, int]:
        coords = np.where(self.game_board == self._PLAYER_FIELD)
        return [coords[0][0], coords[1][0]]

    def _check_if_done(self):
        return np.all(self.game_board != self._FOOD_FIELD)

    def _set_field(self, x, y, value):
        self.game_board[x][y] = value

    def _get_field(self, x, y):
        return self.game_board[x][y]

    def _number_to_symbol(self, number):
        if number == self._EMPTY_FIELD: return " "
        if number == self._PLAYER_FIELD: return "X"
        if number == self._FOOD_FIELD: return "F"
        if number == self._HOLE_FIELD: return "O"

def human_game_loop():
    env = MinimalEnv()

    env.reset()
    env.render()

    done = False

    while not done:
        action = _get_human_input()

        obs, reward, done, info = env.step(action)
        env.render()

    
def _get_human_input() -> directions.Direction:
    action = None
    while action is None:
        choice = input("Enter direction: [0] -> UP, [1] -> LEFT, [2] -> DOWN, [3] -> RIGHT: ")

        # Mapping numbers to directions
        if choice in ["0", "1", "2", "3"]:
            if choice == "0": action = directions.Direction.UP
            if choice == "1": action = directions.Direction.LEFT
            if choice == "2": action = directions.Direction.DOWN
            if choice == "3": action = directions.Direction.RIGHT

        # Allowing names of directions as input
        if choice.upper() in ["UP", "LEFT", "DOWN", "RIGHT"]:
            if choice.upper() == "UP": action = directions.Direction.UP
            if choice.upper() == "LEFT": action = directions.Direction.LEFT
            if choice.upper() == "DOWN": action = directions.Direction.DOWN
            if choice.upper() == "RIGHT": action = directions.Direction.RIGHT

    return action.value

# human_game_loop()


env = MinimalEnv()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log='runs/').learn(1_000_000)

obs = env.reset()
while True:

    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    env.render()
    if done:
        break

env.close()

print("Done!")

sys.exit(0)
for episode in range(1, 2):

    print(f"\n\nEpisode: {episode}")

    obs = env.reset()
    env.render()
    print(f"Initial Observation: {obs}")

    steps = 0

    done = False
    while not done:

        random_action = env.action_space.sample()
        print(f"Action: {random_action}")

        obs, reward, done, info = env.step(random_action)
        env.render()

        print(f"{obs=} {reward=} {done=}")


        steps += 1
        if steps > 5: break
        
