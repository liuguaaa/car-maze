import gym
from stable_baselines3 import DQN
from stable_baselines3.common.noise import NormalActionNoise
import numpy as np
from discrete_env import discrete_CarMazeEnv
import matplotlib.pyplot as plt


env = gym.make("LunarLander-v2", render_mode="human")

# The noise objects for DDPG
n_actions = env.action_space.shape
action_noise = NormalActionNoise(mean=np.zeros(n_actions), sigma=0.1 * np.ones(n_actions))

model = DQN("MlpPolicy", env,
             batch_size=200,
             #buffer_size= 50000,
             exploration_fraction = 0.0001,
             learning_starts = 10000,
             exploration_final_eps = 0.2,
             device='cuda',
             seed=10,
             verbose=1,
             tensorboard_log='./log/dqn')

model.learn(total_timesteps=120000,
            log_interval=1,
            tb_log_name='DQN_car')

model.save("./model/dqn/dqn_1.pkl")



x = np.arange(0, len(env.rewards), 1)
y = np.array(env.rewards)
plt.xlabel("Episodes")
plt.ylabel("Rewards")
plt.plot(x, y, '-*')
plt.savefig("dqn_reward.png")
plt.show()

