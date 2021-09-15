import gym
from gym import Env
from gym.spaces import Discrete, Box, Dict, Tuple, MultiBinary, MultiDiscrete

import numpy as np
import random





#[(0, -1), (0, 1), (1, 0), (-1, 0), (0, 0)]
class LogisticsArea(Env):
    def __init__(self):
        self.action_space = Dict({'direction': Tuple([(0, -1), (0, 1), (1, 0), (-1, 0), (0, 0)]) , 'drop': Discrete(2)})
        self.observation_space = np.array([
            (1, 2, 3, 4, 5),
            (6, 7, 8, 9, 10),
            (11, 12, 13, 14, 15),
            (0, 0, 66, 0, 0)])
        self.state = [0, 3]  # current position
        self.packets = [1, 1, 3, 4, 6, 6, 12, 15, 15, 4, 2, 7, 9, 8, 4, 14, 13, 18, 1, 1, 1, 1, 1]
        self.currentPacket = self.packets.pop()
        self.packet_left = self.packets.__len__()

    def step(self, action):
        reward = 0
        try:
            newState = self.state + action
            # TODO bessere Behlohnung wenn zurückgelete Distanz klein ist
            if self.observation_space[newState] == self.currentPacket & self.action_space['drop'] == 1:
                reward += 1
                self.currentPacket = -1
            if self.observation_space[newState] != self.currentPacket & self.action_space['drop'] == 1:
                reward -= 1
            if self.observation_space[newState] == 66 & self.currentPacket == -1:
                reward += 1
                self.currentPacket = self.packets.pop()

            self.state = self.state + action

        except:
            # out of bounds und self.state ändert sich nicht.
            reward -= 10

        done = self.packet_left <= 0

        info = {}

        return self.state, reward, done, info

    def render(self, mode='human'):
        pass

    def reset(self):
        self.state = [0, 3]  # current position
        self.packets = [1, 1, 3, 4, 6, 6, 12, 15, 15, 4, 2, 7, 9, 8, 4, 14, 13, 18, 1, 1, 1, 1, 1]
        self.packets = [random.randint(0, 10) for _ in range(20)]
        return self.state
