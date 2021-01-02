import math
import os
import sys
from datetime import datetime
from typing import *

import matplotlib.pylab as plt
import numpy as np
import pygame
from tqdm import tqdm

G = 9.8
w, h = 1024, 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LT_BLUE = (230, 230, 255)
offset = (w // 2, h // 4)


class SimplePendulum:
    def __init__(self):
        self.length: float = 1
        self.theta: float = 60
        self.theta_dot: float = 0
        self.dt: float = 0.01
        self.radius: float = 0.01
        self.viscosity: float = 0.0000174
        self.time: float = 0
        self.mass: float = 0.1

    def simulate_with_input(self) -> None:
        self.get_input()
        self.simulate()

    def run_with_input(self) -> Tuple[np.ndarray, np.ndarray]:
        self.get_input()
        time = float(input("time>>"))
        time, theta = self.process(time)
        date = datetime.today().strftime("%Y%m%d-%H%M%S")

        os.makedirs("result/" + date)

        with open("result/" + date + "/time-theta.csv", "w") as f:
            for i in tqdm(range(len(time))):
                f.write(str(time[i]))
                f.write(",")
                f.write(str(theta[i]))
                f.write("\n")
        local_min, local_max = self.get_extreme_value(theta)
        with open("result/" + date + "/time-local_min.csv", "w") as f:
            for i in local_min:
                f.write(str(time[i]))
                f.write(",")
                f.write(str(theta[i]))
                f.write("\n")
        with open("result/" + date + "/time-local_max.csv", "w") as f:
            for i in local_max:
                f.write(str(time[i]))
                f.write(",")
                f.write(str(theta[i]))
                f.write("\n")
        plt.plot(time, theta)
        plt.show()
        return time, theta

    def get_extreme_value(self, values: np.ndarray) -> Tuple[List[float], List[float]]:
        local_min = []
        local_max = []
        for i in tqdm(range(len(values) - 2)):
            if values[i - 1] > values[i] and values[i + 1] > values[i]:
                local_min.append(i)
            if values[i - 1] < values[i] and values[i + 1] < values[i]:
                local_max.append(i)
        return local_min, local_max

    def get_input(self) -> None:
        self.length = float(input("length>>"))
        self.theta = math.radians(float(input("theta>>")))
        self.theta_dot = float(input("theta dot>>"))
        self.dt = float(input("dt>>"))
        self.radius = float(input("radius>>"))
        self.viscosity = float(input("viscosity>>"))
        self.mass = float(input("mass>>"))

    def process(self, max_time: float) -> Tuple[np.ndarray, np.ndarray]:
        times = []
        thetas = []
        for i in tqdm(np.arange(self.time, max_time, self.dt)):
            times.append(i)
            thetas.append(self.theta)

            self.step()

        return np.array(times), np.array(thetas)

    def step(self):
        mu = 6 * math.pi * self.viscosity * self.radius / self.mass
        double_dot_theta = -G / self.length * math.sin(self.theta) - mu * self.theta_dot * self.dt
        self.theta_dot += double_dot_theta * self.dt
        self.theta += self.theta_dot * self.dt

    def simulate(self):
        pygame.init()
        screen = pygame.display.set_mode([w, h])
        clock = pygame.time.Clock()

        fps = int(1 / self.dt)
        print(fps)

        while True:
            clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            coord = offset[0] + 500 * math.sin(self.theta), offset[1] + 500 * math.cos(self.theta)

            screen.fill(WHITE)
            pygame.draw.circle(screen, BLACK, offset, 8)
            pygame.draw.circle(screen, BLUE, coord, 10)
            pygame.draw.line(screen, RED, offset, coord)

            pygame.display.flip()

            self.step()


if __name__ == "__main__":
    obj = SimplePendulum()
    obj.simulate_with_input()
    # theta, time = obj.run_with_input()
    # plt.plot(theta, time)
    # plt.show()
