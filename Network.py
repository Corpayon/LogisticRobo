
from stable_baselines3 import PPO
import os
import Env

env = Env.LogisticsArea()
episodes = 5
for episode in range(1, episodes + 1):
    obs = env.reset()
    done = False
    score = 0

    while not done:
        env.render()
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)
        score += reward
    print('Episode:{} Score {}'.format(episode,score))

env.close()

log_path = os.path.join('Training', 'Logs')
model = PPO('MlpPolicy', env, verbose=1, tensorboard_log=log_path)

model.learn(total_timesteps=50000)

model.save(os.path.join('Training', 'Saved Models', 'LogisticsArea'))
