import pygame, sys
from constants import DISPLAYSURF, disp_height, disp_width
from pygame.locals import *
import random
import numpy as np


class game_env:
    def __init__(self, suffix):
        self.q_table = np.zeros((100, 4))
        self.reward_map = {"hit": -20, "won": 20}
        # self.dir = {0: "left", 2: "right", 1: "down", 3: "up"}
        self.alpha = 0.75
        self.beta = 0.75
        self.greedy = 0
        self.random = 1
        self.delta = 0.005
        self.game_dim = (disp_width, disp_height)
        self.text_space = 150
        self.initial_cood = (0, 0 + self.text_space)
        self.rows, self.columns = 10, 10
        self.start_state = 0
        self.end_state = 99
        # self.cell_dim = self.game_dim[0] / self.rows
        # self.final_cood = (
        #     self.game_dim[0] - self.cell_dim,
        #     self.game_dim[1] - self.cell_dim,
        # )
        # self.game_grid = self.new_game_env()
        self.suffix = suffix
        # self.action_space = {
        #     0: {"x": -1 * self.cell_dim, "y": 0},
        #     2: {"x": self.cell_dim, "y": 0},
        #     1: {"x": 0, "y": self.cell_dim},
        #     3: {"x": 0, "y": -1 * self.cell_dim},
        # }
        try:
            with open("env_weights\\weights_{}.npy".format(self.suffix), "rb") as f:
                self.q_table = np.load(f)
            with open("env_weights\\env_{}.npy".format(self.suffix), "rb") as f:
                self.game_grid = np.load(f)
        except Exception as e:
            print("No such files pre-exists. Starting a new environment")
            with open("env_weights\\env_{}.npy".format(self.suffix), "wb") as f:
                np.save(f, self.game_grid)
            with open("env_weights\\weights_{}.npy".format(self.suffix), "wb") as f:
                np.save(f, self.q_table)
            pass

    # def new_game_env(self):
    #     """
    #     Create new road environment
    #     """
    #     matrix = random.choices(
    #         ["road.png", "traffic.png", "jam.png", "fast.png"],
    #         weights=[0.55, 0.15, 0.15, 0.15],
    #         k=self.rows * self.columns,
    #     )
    #     matrix = np.asarray(matrix).reshape(self.rows, self.columns)
    #     matrix[0][0] = "man.png"
    #     matrix[self.rows - 1][self.columns - 1] = "house.png"
    #     return matrix

    def image_loader(self, img_path):
        """
        Load required icons to display on gaming screen
        """
        img = pygame.image.load("icons\\{}".format(img_path))
        img = pygame.transform.scale(img, (self.cell_dim, self.cell_dim))
        return img

    def print_summary(self, text, cood, size):
        """
        Text to be printed on pygame display screen
        """
        font = pygame.font.Font(pygame.font.get_default_font(), size)
        text_surface = font.render(text, True, (255, 255, 255))
        DISPLAYSURF.blit(text_surface, cood)

    # def initial_state(self):
    #     """
    #     Draw environment on pygame DISPLAYSURF
    #     """
    #     DISPLAYSURF.fill((0, 0, 0))
    #     for x in range(self.rows):
    #         for y in range(self.columns):
    #             img = self.image_loader(self.game_grid[x][y])
    #             cood = (y * self.cell_dim, x * self.cell_dim + self.text_space)
    #             DISPLAYSURF.blit(img, cood)
    #     self.print_summary("Traffic Turbo", (175, 25), 24)
    #     pygame.display.update()

    def steps_visualizer(self, cood):
        """
        Draw steps for each action taken on pygame screen
        """
        img = pygame.image.load("icons\\feet.png")
        img = pygame.transform.scale(img, (self.cell_dim, self.cell_dim))
        DISPLAYSURF.blit(img, cood)
        pygame.display.update()
        clock.tick(1)

    def cood_state_calc(self, cood):
        """
        Calculate game state using pygame screen coordinates
        """
        state = int(
            (self.rows * (cood[1] - self.text_space) / self.cell_dim)
            + (cood[0] / self.cell_dim)
        )
        return state

    def state_cood_calc(self, state):
        """
        Calculate pygame screen coordinates using game state
        """
        cood = int((state % self.rows) * self.cell_dim), int(
            (state // self.rows) * self.cell_dim + self.text_space
        )
        return cood

    def is_valid_move(self, cood, already_visited):
        """
        Check move validity. If not valid, terminate episode
        """

        if cood in already_visited:
            return False

        if (
            self.initial_cood[0] <= cood[0] <= self.final_cood[0]
            and self.initial_cood[1] <= cood[1] <= self.final_cood[1]
        ):
            return True
        return False

    def q_table_update(self, state, action, already_visited):
        """
        Update Q-Table according to action taken
        """
        # curr_cood = self.state_cood_calc(state)
        # new_cood = (
        #     int(curr_cood[0] + self.action_space[action]["x"]),
        #     int(curr_cood[1] + self.action_space[action]["y"]),
        # )
        # new_state = self.cood_state_calc(new_cood)
        # is_valid = self.is_valid_move(new_cood, already_visited)

        # if is_valid:
        act = "hit" if (self.action == 0) else "won"
        reward = self.reward_map[act]
        # elif new_cood in already_visited:
        #     reward = self.reward_map["already_visited"]
        # else:
        #     reward = self.reward_map["invalid"]

        try:
            state_value_diff = (
                max(self.q_table[new_state]) - self.q_table[state][action]
            )
        except:
            state_value_diff = 0
        self.q_table[state][action] += self.alpha * (
            reward + self.beta * state_value_diff
        )

        return is_valid, new_state, new_cood, reward

    def episode(self, current_state, is_valid):
        """
        Intiate an episode while training
        """
        pygame.event.get()
        cood = self.state_cood_calc(current_state)
        already_visited = [cood]
        self.steps_visualizer(cood)

        while current_state != self.end_state and is_valid == True:
            pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (0, 100, self.game_dim[0], 50))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise Exception("training ended")
            choice = random.choices(
                [True, False], weights=[self.greedy, self.random], k=1
            )
            if choice[0]:
                action = np.argmax(self.q_table[current_state])
            else:
                action = random.choices(
                    [0, 1, 2, 3], weights=[0.25, 0.25, 0.25, 0.25], k=1
                )
                action = action[0]
            self.print_summary("State:{}".format(current_state), (10, 100), 15)
            self.print_summary("Action:{}".format(self.dir[action]), (110, 100), 15)
            is_valid, current_state, cood, reward = self.q_table_update(
                current_state, action, already_visited
            )

            self.print_summary("Reward:{}".format(reward), (220, 100), 15)

            if is_valid == False and cood not in already_visited:
                self.print_summary("INVALID MOVE !!", (330, 100), 15)
            elif is_valid == False:
                self.print_summary("ALREADY VISITED", (330, 100), 15)
            else:
                self.print_summary("New State:{}".format(current_state), (330, 100), 15)

            pygame.display.update()
            clock.tick(0.9)
            already_visited.append(cood)
            if is_valid:
                self.steps_visualizer(cood)
            else:
                break

    def training(self, epoch):
        state = random.randint(self.start_state, self.end_state)
        self.initial_state()
        self.print_summary(" Episode:{}".format(epoch), (200, 60), 20)
        self.episode(state, True)
        print("episode {} ---->".format(epoch))
        pygame.display.set_caption(
            "greedy={}, random={}".format(round(self.greedy, 4), round(self.random, 4))
        )
        if epoch % 50 == 0:
            if self.random > 0:
                self.greedy += self.delta
                self.random -= self.delta
                self.greedy = min(self.greedy, 1)
                self.random = max(self.random, 0)

        if epoch % 2000 == 0:
            self.delta *= 2
            with open("env_weights\\weights_{}.npy".format(self.suffix), "wb") as f:
                np.save(f, self.q_table)

        clock.tick(1)

    def testing(self, initial_state=0):
        self.greedy = 1
        self.random = 0
        with open("env_weights\\env_{}.npy".format(self.suffix), "rb") as f:
            self.game_grid = np.load(f)

        with open("env_weights\\weights_{}.npy".format(self.suffix), "rb") as f:
            self.q_table = np.load(f)

        self.initial_state()
        self.episode(initial_state, True)
