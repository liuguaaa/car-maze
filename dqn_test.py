from matplotlib.ticker import FuncFormatter
from mpl_toolkits import axisartist
from stable_baselines3 import DDPG, PPO,SAC,DQN
from discrete_env import discrete_CarMazeEnv
import pygame
from PIL import ImageGrab
from stable_baselines3.common.evaluation import evaluate_policy
from maze_env import CarMazeEnv
import matplotlib.pyplot as plt
import numpy as np
import math


env = discrete_CarMazeEnv()

model = DQN.load("model/dqn/dqn_2.pkl",env=env)

state = env.reset()

# receiverAngles = []
# buoyAngles = []
# prs = []
# intensities = []
# snr = []
# intensities_stand = []
# snr_stand = []
# energyConsumption = []
# rates = []
for i in range(10):
        j = 0
        while True:
            action, _ = model.predict(observation=state)
            state, reward, done, info = env.step(action)
            env.render()
            if done:
                break
            screen_content = pygame.display.get_surface()
            pygame.image.save(screen_content,'episode{}_screenshot{}.png'.format(i+1,j))
            j += 1
        env.reset()


