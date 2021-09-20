from stable_baselines3 import PPO
import os
import Env
import gym
# eigene space https://stackoverflow.com/questions/56533094/openai-gym-custom-environment-discrete-observation-space-with-real-values
env = Env.LogisticsArea()
episodes = 5
for episode in range(1, episodes + 1):
    obs = env.reset()
    done = False
    score = 0

    while not done:
        env.render()
        action = env.action_space.sample()
        game_board, reward, done, info = env.step(action)
        score += reward

    print('Episode:{} Score {}'.format(episode, score))

env.close()

model = PPO('MlpPolicy', env, verbose=1, tensorboard_log='runs/').learn(1000000)


#model.save(os.path.join('Training', 'Saved Models', 'LogisticsArea'))
