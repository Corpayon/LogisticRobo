from enum import Enum
from typing import Type

import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete

import numpy as np
import random

from DirectionSpace import DirectionSpace


class LogisticsArea(Env):
    def __init__(self):
        self.action_space = MultiDiscrete([5,2])
        self.observation_space = Box(0, 66, shape=(4,5))
        self.state = [0, 3]  # current position
        self.packets = [random.randint(0, 15) for _ in range(4)]
        self.currentPacket = self.packets[0]
        self.increment = 0
        self.packet_left = self.packets.__len__()
        self.DirectionList = ((0,1),(0,-1),(-1,0),(1,0),(0,0))

    def step(self, action):
        reward = 0

        try:
            direction = self.DirectionList.__getitem__(action[0])
            newState = [self.state[0] + direction[0], self.state[1] + direction[1]]

            # TODO bessere Behlohnung wenn zurückgelete Distanz klein ist
            if self.game_board[newState[0]][newState[1]] == self.currentPacket and action[1] == 1:
                reward += 1
                self.currentPacket = -1
            if self.game_board[newState[0]][newState[1]] != self.currentPacket and action[1] == 1:
                reward -= 1
            if self.game_board[newState[0]][newState[1]] == 66 and self.currentPacket == -1:
                reward += 1
                self.increment += 1
                self.currentPacket = self.packets[self.increment]


            self.state = [self.state[0] + direction[0], self.state[1] + direction[1]]
           # if self.observation_space[newState[0]][newState[1]] == 1: print(self.observation_space[newState[0]][newState[1]])

        except:
            # out of bounds und self.state ändert sich nicht.
            reward +=0

        done = self.packet_left == self.increment


        info = {}

        return self.game_board,reward, done, info

    def render(self, mode='human'):
        pass

    def reset(self):
        self.state = [0, 3]  # current position
        self.packets = [random.randint(0, 15) for _ in range(4)]
        self.currentPacket = self.packets[0]
        self.increment = 0
        self.game_board = np.array([
            (1, 2, 3, 4, 5),
            (6, 7, 8, 9, 10),
            (11, 12, 13, 14, 15),
            (0, 0, 66, 0, 0)])
        return self.game_board
