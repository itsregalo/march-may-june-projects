# the definition of the Agent

import numpy as np
import matplotlib.pyplot as plt
import random
from collections import namedtuple, deque

from algorithms.pytorch_model import QNetwork
import matplotlib as mpl

import torch
import torch.nn.functional as nn_functional
import torch.optim as torch_optimization

BUFFER_SIZE = int(1e1)  # replay buffer size  # int(1e5)
BATCH_SIZE = 2         # mini-batch size  # 64
GAMMA = 0.9             # discount factor  # 0.99
TAU = 1e-3              # for soft update of target parameters  # 1e-3
LR = 5e-4               # learning rate # 5e-4
UPDATE_EVERY = 1        # how often to update the network  # 4

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


class Agent:
    """Interacts with and learns from the environment."""

    def __init__(self, actions, state, seed=0):
        self.actions_list = actions
        self.state_features_list = state
        state_size = len(state)
        action_size = len(actions)

        self.action_size = action_size
        self.state_size = state_size
        self.seed = random.seed(seed)

        # define Q-Network
        self.q_network_local = QNetwork(state_size, action_size, seed).to(device)
        self.q_network_target = QNetwork(state_size, action_size, seed).to(device)

        # define optimizer
        # specify the tensors that should be optimized: q_network_local. Not q_network_target!
        # learning rate (default: 1e-3)
        self.optimizer = torch_optimization.Adam(params=self.q_network_local.parameters(), lr=LR)
        # ToDo: Adjust Learning Rate
        self.memory = ReplayBuffer(action_size, BUFFER_SIZE, BATCH_SIZE, seed)
        # Initialize time step (for updating every UPDATE_EVERY steps)
        self.t_step = 0

        # for debug
        self.state_view_counter = np.zeros((20, 5))
        self.v_table = np.zeros((20, 5))
        self.count_state_counter = 1

    @staticmethod
    def state_processing(state):
        return [state[0] / 20, state[1] / 5]

    def step(self, state, action, reward, next_state, done):
        """ Save a transition """
        action_id = self.actions_list.index(action)

        # Save experience in replay memory
        state = self.state_processing(state)
        next_state = self.state_processing(next_state)
        self.memory.add(state, action_id, reward, next_state, done)
        
        # Learn every UPDATE_EVERY time steps.
        self.t_step = (self.t_step + 1) % UPDATE_EVERY
        if self.t_step == 0:
            # If enough samples are available in memory, get random subset and learn
            if len(self.memory) > BATCH_SIZE:
                # print("get random subset and learn")
                experiences = self.memory.sample()
                self.learn(experiences, GAMMA)

    def save_q_table(self, folder):
        torch.save(self.q_network_local.state_dict(), folder+'checkpoint.pth')

    def print_parameters_nn(self):
        print(self.q_network_local)
        print(self.q_network_local.fc1.weight)
        print(self.q_network_local.fc2.weight)
        print(self.q_network_local.fc3.weight)
        print(self.q_network_local.fc1.bias)
        print(self.q_network_local.fc2.bias)
        print(self.q_network_local.fc3.bias)

    def count_state(self, state):
        self.count_state_counter += 1
        # print(self.count_state_counter)
        # print(state)
        self.state_view_counter[tuple(state)] += 1
        if self.count_state_counter % 1000 == 0:
            print("{} experiences seen".format(self.count_state_counter))
            # set the visitation of the init to 0 (otherwise, we do not see the others)
            self.state_view_counter[tuple([0, 3])] = 0
            self.plot_count_state()

            self.get_v_value_map()
            self.plot_v_value_map()

    def get_v_value_map(self):
        for pos in range(20):
            for vel in range(5):
                state = [pos, vel]
                state = self.state_processing(state)
                state = np.array(state)
                state = torch.from_numpy(state).float().unsqueeze(0).to(device)

                # read local estimate
                self.q_network_local.eval()
                with torch.no_grad():
                    action_values = self.q_network_local(state)
                self.q_network_local.train()

                actions_values = action_values.cpu().data.numpy()
                actions_values = actions_values[0]

                self.v_table[pos, vel] = np.max(actions_values)

    def plot_v_value_map(self):

        # setup the plot
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))

        # define the data
        data = self.v_table
        # define the colormap
        cmap = plt.cm.jet
        # extract all colors from the .jet map
        cmaplist = [cmap(i) for i in range(cmap.N)]
        # create the new map
        cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

        # define the bins and normalize
        # print("np.max(data) = {}".format(np.max(data)))
        bounds = np.linspace(np.min(self.v_table), np.max(self.v_table), 21)
        # print(bounds)

        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        plt.imshow(data, cmap=cmap, interpolation='nearest')
        ticks = [str(round(elem, 3)) for elem in bounds]
        ax2 = fig.add_axes([0.7, 0.1, 0.03, 0.8])  # [left, bottom, width, height]
        mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', boundaries=bounds,
                                  format='%1i')

        ax2.set_yticklabels(ticks)
        ax.set_title("v_values")
        ax2.set_ylabel('v_values', size=12)

        ax.set_xticks(np.arange(-.5, 5, 1))
        ax.set_yticks(np.arange(-.5, 20, 1))
        ax.set_xticklabels(np.arange(0, 5, 1))
        ax.set_yticklabels(np.arange(0, 20, 1))

        ax.grid()
        # plt.show()
        plt.savefig('v_values/'+str(self.count_state_counter) + '_steps.png')
        fig.close()

    def plot_count_state(self):
        # setup the plot
        fig, ax = plt.subplots(1, 1, figsize=(6, 6))

        # define the data
        data = self.state_view_counter
        # define the colormap
        cmap = plt.cm.jet
        # extract all colors from the .jet map
        cmaplist = [cmap(i) for i in range(cmap.N)]
        # force the first color entry to be grey
        cmaplist[0] = (.5, .5, .5, 1.0)
        # create the new map
        cmap = cmap.from_list('Custom cmap', cmaplist, cmap.N)

        # define the bins and normalize
        # print("np.max(data) = {}".format(np.max(data)))
        bounds = np.linspace(0, np.max(data), 21)

        norm = mpl.colors.BoundaryNorm(bounds, cmap.N)

        # make the im_show()
        plt.imshow(data, cmap=cmap, interpolation='nearest')

        # create a second axes for the colorbar
        ax2 = fig.add_axes([0.7, 0.1, 0.03, 0.8])  # [left, bottom, width, height]
        mpl.colorbar.ColorbarBase(ax2, cmap=cmap, norm=norm, spacing='proportional', ticks=bounds, boundaries=bounds,
                                  format='%1i')

        ax.set_title('after ' + str(self.count_state_counter) + ' steps')
        ax2.set_ylabel('occurrence', size=12)

        ax.set_xticks(np.arange(-.5, 5, 1))
        ax.set_yticks(np.arange(-.5, 20, 1))
        ax.set_xticklabels(np.arange(0, 5, 1))
        ax.set_yticklabels(np.arange(0, 20, 1))

        ax.grid()

    def choose_action(self, state, masked_actions_list, greedy_epsilon):  # act()

        # Creates a torch Tensor from a numpy.ndarray
        # print("choose_action in state = {}".format(state))
        self.count_state(state)
        state = self.state_processing(state)
        state = np.array(state)
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)

        # Sets the module in evaluation mode
        self.q_network_local.eval()

        # Disabling gradient calculation is useful for inference, when you know that you will not call Tensor.backward()
        with torch.no_grad():
            # read values from function approximation
            action_values = self.q_network_local(state)

        # Sets the module in training mode.
        self.q_network_local.train()

        possible_actions = [action for action in self.actions_list if action not in masked_actions_list]

        # Epsilon-greedy action selection
        if random.random() > greedy_epsilon:

            # Retrieve a tensor held by the Variable action_values.cpu(), using the .data attribute
            actions_values = action_values.cpu().data.numpy()
            actions_values = actions_values[0]

            for action in self.actions_list:
                if action not in possible_actions:
                    action_id = self.actions_list.index(action)
                    actions_values[action_id] = -np.inf

            # make decision
            if np.all(np.isneginf([actions_values])):
                action_id = random.choice(possible_actions)
            else:
                action_id = np.argmax(actions_values)
            selected_action = self.actions_list[action_id]
        else:
            selected_action = random.choice(possible_actions)

        return selected_action

    def compare_reference_value(self):
        # ToDo: we know the value of the last-but one state at convergence: Q(s,a)=R(s,a).
        state = [16, 3]
        action_id = 0
        state = self.state_processing(state)
        state = np.array(state)
        state = torch.from_numpy(state).float().unsqueeze(0).to(device)

        # read local estimate
        self.q_network_local.eval()
        with torch.no_grad():
            action_values = self.q_network_local(state)
        self.q_network_local.train()

        actions_values = action_values.cpu().data.numpy()
        actions_values = actions_values[0]

        print("q_values for [state = [16, 3]] = {}".format(actions_values))
        return action_values[action_id]

    def learn(self, experiences, gamma):

        states, actions, rewards, next_states, dones = experiences

        # Get max predicted Q valueS (for EACH next state) from target model
        # use detach() to get a new Tensor, detached from the current graph.
        q_targets_next = self.q_network_target(next_states).detach().max(1)[0].unsqueeze(1)

        # Compute Q targets for current states
        q_targets = rewards + (gamma * q_targets_next * (1 - dones))
        # print("rewards = {}".format(rewards))

        # Get expected Q values from local model - gather() gathers values along an axis specified by dim
        q_expected = self.q_network_local(states).gather(1, actions)

        # Compute loss

        loss = nn_functional.mse_loss(q_expected, q_targets)  # the element-wise mean squared error

        # Minimize the loss
        self.optimizer.zero_grad()  # Clears the gradients of all optimized torch.Tensors
        # Computes the gradient of current tensor w.r.t. graph leaves.
        loss.backward()  # the gradients are computed
        self.optimizer.step()  # step() method, that updates the parameters

        # test if the update can also increase expectations in the local model

        # ToDo: why "change in q_expected" is not consistent with td_error? Especially for positive td_errors

        # ------------------- update target network ------------------- #
        self.soft_update(self.q_network_local, self.q_network_target, TAU)
        print("-- --\n")

    @staticmethod
    def soft_update(local_model, target_model, tau):
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)


class ReplayBuffer:
    """Fixed-size buffer to store experience tuples."""

    def __init__(self, action_size, buffer_size, batch_size, seed):
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)  
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=["state", "action", "reward", "next_state", "done"])
        self.seed = random.seed(seed)
    
    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)
    
    def sample(self):
        """Randomly sample a batch of experiences from memory."""
        experiences = random.sample(self.memory, k=self.batch_size)

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)
  
        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)