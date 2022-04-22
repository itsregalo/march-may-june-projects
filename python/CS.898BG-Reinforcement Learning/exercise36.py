# pole-balancing as an episodic task but also useddiscounting, with all rewards zero except for 1 upon failure.

import gym
import numpy as np
import matplotlib.pyplot as plt
from gym import wrappers
from gym.envs.registration import register
from time import sleep

#Agent
class Agent:
    def __init__(self, env):
        self.env = env
        self.state = env.reset()
        self.action_space = env.action_space
        self.observation_space = env.observation_space
        self.action_size = self.action_space.n
        self.state_size = self.observation_space.shape[0]
        self.discount_factor = 0.99
        self.learning_rate = 0.001
        self.epsilon = 1.0
        self.epsilon_decay = 0.999
        self.epsilon_min = 0.01
        self.batch_size = 64
        self.train_start = 1000
        self.memory = []
        self.train_step = 0
        self.loss_list = []
        self.q_table = np.zeros((self.state_size, self.action_size))

    def get_action(self, state):
        if np.random.rand() <= self.epsilon:
            return self.action_space.sample()
        else:
            return np.argmax(self.q_table[state, :])

    def update_q_table(self, state, action, reward, next_state, done):
        q_predict = self.q_table[state, action]
        if done:
            q_target = reward
        else:
            q_target = reward + self.discount_factor * np.max(self.q_table[next_state, :])
        self.q_table[state, action] += self.learning_rate * (q_target - q_predict)

    def train(self):
        if len(self.memory) < self.train_start:
            return
        batch_size = min(self.batch_size, len(self.memory))
        mini_batch = np.random.choice(self.memory, batch_size)
        for state, action, reward, next_state, done in mini_batch:
            self.update_q_table(state, action, reward, next = next_state, done = done)
        self.train_step += 1
        if self.train_step % 100 == 0:
            self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)
            print("epsilon:", self.epsilon)

    def save_q_table(self):
        np.save("q_table.npy", self.q_table)
        


# register the pole environment from OpenAI gym
register(
    id='CartPole-v0',
    entry_point='gym.envs.classic_control:CartPoleEnv',
    max_episode_steps=200,
    reward_threshold=195.0,
)

# create the environment
env = gym.make('CartPole-v0')

# create the agent
agent = Agent(env)

# run the agent
agent.run()

# plot the results
agent.plot()