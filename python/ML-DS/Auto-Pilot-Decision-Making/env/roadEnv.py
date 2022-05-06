
import time
import numpy as np  # but trying to avoid using it (np.array cannot be converted to JSON)
import tkinter as tk
from utils.logger import Logger

UNIT = 20   # pixels per grid cell
MAZE_H = 4  # grid height
MAZE_W = 20  # grid width  !! Adapt the threshold_success in the main accordingly
HALF_SIZE = UNIT * 0.35  # half size factor of square in a cell
Y_COORD = 0  # blocking motion of ego agent in one row - no vertical motion allowed


def one_hot_encoding(feature_to_encode):
    repr_size = MAZE_W
    one_hot_list = np.zeros(repr_size)
    # one_hot_list = [0] * UNIT
    if feature_to_encode < repr_size:
        one_hot_list[feature_to_encode] = 1
    else:
        print('feature is out of scope for one_hot_encoding: %i / %i' % (feature_to_encode, repr_size))
    # print(one_hot_list)
    return one_hot_list


def process_state(input_state):
    ego_position = input_state[0]
    velocity = input_state[1]
    # obstacle_position = input_state[2]
    #
    # # one-hot encoding of the state

    # ToDo: increase state for the brain
    return [ego_position, velocity]  # , obstacle_position]

    # make one_hot_state have mean 0 and a variance of 1


# !! Depending is tk is supported or not, manually change the inheritance
# !! uncomment the next line and comment the two next
# class Road:  # if tk is NOT supported. Then make sure using_tkinter=False
class Road(tk.Tk, object):  # if tk is supported
    def __init__(self, using_tkinter, actions_names, state_features, initial_state, goal_velocity=4):
        # graphical interface
        if using_tkinter:
            super(Road, self).__init__()

        # action space
        self.actions_list = actions_names

        # state is composed of
        # - absolute ego_position
        # - velocity
        # - absolute position of obstacle
        self.state_features = state_features

        # Reward - the reward is update
        # - during the transition (hard-constraints)
        # - in the reward_function (only considering the new state)
        self.reward = 0
        self.rewards_dict = {
            # efficiency = Progress
            "goal_with_good_velocity": 40,
            "goal_with_bad_velocity": -40,
            "per_step_cost": -3,
            "under_speed": -15,

            # traffic law
            "over_speed": -10,
            "over_speed_2": -10,

            # safety
            "over_speed_near_pedestrian": -40,

            # Comfort
            "negative_speed": -15,
            "action_change": -2
        }

        self.max_velocity_1 = 4
        self.max_velocity_2 = 2
        self.max_velocity_pedestrian = 2
        self.min_velocity = 0

        # state - for the moment distinct variables
        self.initial_state = initial_state
        self.state_ego_position = self.initial_state[0]
        self.state_ego_velocity = self.initial_state[1]
        self.state_obstacle_position = self.initial_state[2]
        self.previous_state_position = self.state_ego_position
        self.previous_state_velocity = self.state_ego_velocity
        self.previous_action = None

        # environment:
        self.goal_coord = [MAZE_W - 1, 1]
        self.goal_velocity = goal_velocity
        self.obstacle1_coord = [self.state_obstacle_position, 2]
        self.obstacle2_coord = [1, 3]
        self.initial_position = [self.initial_state[0], Y_COORD]

        # adjusting the colour of the agent depending on its speed
        colours_list = ["white", "yellow", "orange", "red2", "red3", "red4", "black", "black", "black", "black",
                        "black", "black"]
        velocity_list = range(len(colours_list)+1)
        self.colour_velocity_code = dict(zip(velocity_list, colours_list))

        # graphical interface
        self.using_tkinter = using_tkinter
        # create the origin point in  the Tk frame
        self.origin_coord = [(x + y) for x, y in zip(self.initial_position, [0.5, 0.5])]
        # self.origin = UNIT * self.origin_coord
        self.origin = [x * UNIT for x in self.origin_coord]
        self.canvas = None
        self.rect = None
        self.obstacle = None


        if self.using_tkinter:
            # Tk window
            self.title('road')
            self.geometry('{0}x{1}'.format(MAZE_W * UNIT, MAZE_H * UNIT))
            self.build_road()

        # logging configuration
        self.logger = Logger("road", "road_env.log", 0)

    @staticmethod
    def sample_position_obstacle():
        fix_position_obstacle = 12
        return fix_position_obstacle
        # random_position_obstacle = random.randint(1, MAZE_W)
        # random_position_obstacle = random.randint(MAZE_W//2 - 1, MAZE_W//2 + 2)
        # print("{} = random_position_obstacle".format(random_position_obstacle))
        # return random_position_obstacle

    def build_road(self):

        if self.using_tkinter:

            # create canvas
            self.canvas = tk.Canvas(self, bg='white', height=MAZE_H * UNIT, width=MAZE_W * UNIT)

            # create grids
            for c in range(0, MAZE_W * UNIT, UNIT):
                x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
                self.canvas.create_line(x0, y0, x1, y1)
            for r in range(0, MAZE_H * UNIT, UNIT):
                x0, y0, x1, y1 = 0, r, MAZE_W * UNIT, r
                self.canvas.create_line(x0, y0, x1, y1)

            # create ego agent
            self.rect = self.canvas.create_rectangle(
                self.origin[0] - HALF_SIZE, self.origin[1] - HALF_SIZE,
                self.origin[0] + HALF_SIZE, self.origin[1] + HALF_SIZE,
                fill='white')

            # obstacle1
            obstacle1_center = np.asarray(self.origin) + UNIT * np.asarray(self.obstacle1_coord)
            self.obstacle = self.canvas.create_rectangle(
                obstacle1_center[0] - HALF_SIZE, obstacle1_center[1] - HALF_SIZE,
                obstacle1_center[0] + HALF_SIZE, obstacle1_center[1] + HALF_SIZE,
                fill='black')

            # obstacle2
            obstacle2_center = np.asarray(self.origin) + UNIT * np.asarray(self.obstacle2_coord)
            self.canvas.create_rectangle(
                obstacle2_center[0] - HALF_SIZE, obstacle2_center[1] - HALF_SIZE,
                obstacle2_center[0] + HALF_SIZE, obstacle2_center[1] + HALF_SIZE,
                fill='black')

            # create oval for the goal
            goal_center = np.asarray(self.origin) + UNIT * np.asarray(self.goal_coord)
            self.canvas.create_oval(
                goal_center[0] - HALF_SIZE, goal_center[1] - HALF_SIZE,
                goal_center[0] + HALF_SIZE, goal_center[1] + HALF_SIZE,
                fill='yellow')

            # pack all
            self.canvas.pack()

    def reset(self):
        """
        Clean the canvas (remove agent)
        Clean the state (reinitialize it)
        Sample a random position for the obstacle
        :return: the initial state amd the list of the masked actions
        """
        time.sleep(0.005)
        random_position_obstacle = self.sample_position_obstacle()
        self.obstacle1_coord = [random_position_obstacle, 2]

        if self.using_tkinter:
            self.canvas.delete(self.rect)
            self.rect = self.canvas.create_rectangle(
                self.origin[0] - HALF_SIZE, self.origin[1] - HALF_SIZE,
                self.origin[0] + HALF_SIZE, self.origin[1] + HALF_SIZE,
                fill='white')

            self.canvas.delete(self.obstacle)
            obstacle1_center = np.asarray(self.origin) + UNIT * np.asarray(self.obstacle1_coord)
            self.obstacle = self.canvas.create_rectangle(
                obstacle1_center[0] - HALF_SIZE, obstacle1_center[1] - HALF_SIZE,
                obstacle1_center[0] + HALF_SIZE, obstacle1_center[1] + HALF_SIZE,
                fill='black')

        self.state_ego_position = self.initial_state[0]
        self.state_ego_velocity = self.initial_state[1]
        self.state_obstacle_position = random_position_obstacle
        self.initial_state[2] = random_position_obstacle
        self.previous_state_position = self.initial_state[0]
        self.previous_state_velocity = self.initial_state[1]

        return process_state(self.initial_state), self.masking_function()

    def transition(self, action, velocity=None):
        if velocity is None:
            velocity = self.state_ego_velocity

        delta_velocity = 0

        if action == self.actions_list[0]:  # maintain velocity
            delta_velocity = 0
        elif action == self.actions_list[1]:  # accelerate
            delta_velocity = 1
        elif action == self.actions_list[2]:  # accelerate a lot
            delta_velocity = 2
        elif action == self.actions_list[3]:  # slow down
            delta_velocity = -1
        elif action == self.actions_list[4]:  # slow down a lot
            delta_velocity = -2

        return velocity + delta_velocity

    def step(self, action):
        self.previous_state_velocity = self.state_ego_velocity
        self.previous_state_position = self.state_ego_position
        self.previous_action = action

        # Transition = get the new state:
        self.state_ego_velocity = self.transition(action)
        if self.state_ego_velocity < 0:
            self.state_ego_velocity = 0
            message = "self.state_ego_velocity cannot be < 0 - a = {} - p = {} - v = {} " \
                      "in step()".format(action, self.state_ego_position, self.state_ego_velocity)
            self.logger.log(message, 3)

        # Assume simple relation: velocity expressed in [step/sec] and time step = 1s
        desired_position_change = self.state_ego_velocity

        # convert information from velocity to the change in position = number of steps
        tk_update_steps = [0, 0]

        # update the state - position
        self.state_ego_position = self.state_ego_position + desired_position_change
        tk_update_steps[0] += desired_position_change * UNIT

        if self.using_tkinter:
            # move agent in canvas
            self.canvas.move(self.rect, tk_update_steps[0], tk_update_steps[1])
            # update colour depending on speed
            new_colour = self.colour_velocity_code[self.state_ego_velocity]
            self.canvas.itemconfig(self.rect, fill=new_colour)

        # observe reward
        [reward, termination_flag] = self.reward_function(action)

        # for the next decision, these actions are not possible (it uses the output state):
        if termination_flag:
            masked_actions_list = []
        else:
            masked_actions_list = self.masking_function()

        state_to_return = process_state(
            [self.state_ego_position, self.state_ego_velocity, self.state_obstacle_position]
        )
        return state_to_return, reward, termination_flag, masked_actions_list

    def reward_function(self, action):
        # reward put to for the new step
        self.reward = 0

        # penalizing changes in action
        # it penalizes big changes (e.g. from speed_up_up to slow_down_down)
        if self.state_ego_velocity != self.previous_state_velocity:
            change_in_velocity = self.state_ego_velocity - self.previous_state_velocity
            self.reward += self.rewards_dict["action_change"] * abs(change_in_velocity)

        # test about the position
        # - for the goal
        if self.state_ego_position >= self.goal_coord[0]:
            # not over-exceeding the goal
            self.state_ego_position = self.goal_coord[0]
            if self.state_ego_velocity == self.goal_velocity:
                self.reward += self.rewards_dict["goal_with_good_velocity"]
            else:
                self.reward += self.rewards_dict["goal_with_bad_velocity"]
            termination_flag = True

        # - for all other states
        else:
            self.reward += self.rewards_dict["per_step_cost"]
            termination_flag = False

        # check max speed limitation
        if self.state_ego_velocity > self.max_velocity_1:
            excess_in_velocity = self.state_ego_velocity - self.max_velocity_1
            self.reward += self.rewards_dict["over_speed"] * excess_in_velocity
            message = "Too fast! in reward_function() -- hard constraints should have masked it. " \
                      "a = {} - p = {} - v = {}".format(action, self.state_ego_position, self.state_ego_velocity)
            self.logger.log(message, 3)

        # check minimal speed
        if self.state_ego_velocity < self.min_velocity:
            excess_in_velocity = self.min_velocity - self.state_ego_velocity
            # well, basically, it will stay as rest - but still, we need to prevent negative speeds
            self.reward += self.rewards_dict["under_speed"] * excess_in_velocity

            if self.state_ego_velocity < 0:
                excess_in_velocity = abs(self.min_velocity)
                message = "Under speed! in reward_function() -- hard constraints should have masked it. " \
                          "a = {} - p = {} - v = {}".format(action, self.state_ego_position, self.state_ego_velocity)
                self.logger.log(message, 3)

                self.state_ego_velocity = 0
                self.reward += self.rewards_dict["negative_speed"] * excess_in_velocity

        # limit speed when driving close to a pedestrian
        if self.previous_state_position <= self.obstacle1_coord[0] <= self.state_ego_position:
            if self.state_ego_velocity > self.max_velocity_pedestrian:
                excess_in_velocity = self.state_ego_velocity - self.max_velocity_pedestrian
                self.reward += self.rewards_dict["over_speed_near_pedestrian"] * excess_in_velocity
                message = "Too fast close to obstacle! in reward_function() - a = {} - p = {} - po= {} - v = {}".format(
                    action, self.state_ego_position, self.state_obstacle_position, self.state_ego_velocity)
                self.logger.log(message, 1)


        return self.reward, termination_flag

    def masking_function(self, state=None):
        # masking actions that are not possible

        if state is None:
            velocity = None
        else:
            velocity = state[1]

        masked_actions_list = []

        # check if maximum / minimum speed has been reached
        for action_candidate in self.actions_list:
            # simulation for each action
            velocity_candidate = self.transition(action_candidate, velocity)
            # print(velocity_candidate)
            if velocity_candidate > self.max_velocity_1:
                # print("hard _ constraint : to fast")
                masked_actions_list.append(action_candidate)
            elif velocity_candidate < 0:
                # print("hard _ constraint : negative speed")
                masked_actions_list.append(action_candidate)

        # checking there are still possibilities left:
        if masked_actions_list == self.actions_list:
            print("WARNING - velocity %s and position %s" % (self.state_ego_velocity, self.state_ego_position))
            message = "No possible_action found! in masking_function() - a = {} - p = {} - po= {} - v = {}".format(
                self.previous_action, self.state_ego_position, self.state_obstacle_position, self.state_ego_velocity)
            self.logger.log(message, 4)

        return masked_actions_list

    def move_to_state(self, state):
        # move to a given state
        self.state_ego_position = state[0]
        self.state_ego_velocity = state[1]
        pass

    def render(self, sleep_time):
        if self.using_tkinter:
            time.sleep(sleep_time)
            self.update()


def demo(actions, nb_episodes_demo):
    for t in range(nb_episodes_demo):
        _, masked_actions_list = env.reset()
        print("New Episode")
        while True:
            sleep_time = 0.5
            if env.using_tkinter:
                env.render(sleep_time)

            # Pick randomly an action among non-masked actions

            # possible_actions = [action for action in actions]
            possible_actions = [action for action in actions if action not in masked_actions_list]
            if not possible_actions:
                print("!!!!! WARNING - No possible_action !!!!!")
            action = np.random.choice(possible_actions)

            # Give the action to the environment and observe new state and reward
            state, reward, termination_flag, masked_actions_list = env.step(action)
            print("Action=", action, " -- State=", state, " -- Reward=", reward, " -- Termination_flag=",
                  termination_flag, sep='')

            # Check end of episode
            if termination_flag:
                break


if __name__ == '__main__':
    flag_tkinter = True
    nb_episodes = 5
    actions_list = ["no_change", "speed_up", "speed_up_up", "slow_down", "slow_down_down"]
    state_features_list = ["position", "velocity"]
    the_initial_state = [0, 3, 12]
    env = Road(flag_tkinter, actions_list, state_features_list, the_initial_state)
    # Wait 100 ms and run several episodes
    if flag_tkinter:
        env.after(100, demo, actions_list, nb_episodes)
        env.mainloop()  # need to be close manually
    else:
        demo(actions_list, nb_episodes)