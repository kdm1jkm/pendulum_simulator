import math
import sys
from typing import Tuple

import numpy as np
import pygame
from tqdm import tqdm

import matplotlib.pylab as plt

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

    def simulate_with_input(self) -> None:
        self.get_input()
        self.simulate()

    def run_with_input(self) -> Tuple[np.ndarray, np.ndarray]:
        self.get_input()
        t = float(input("time>>"))
        theta, time = self.process(t)
        plt.plot(theta, time)
        plt.show()
        return theta, time

    def get_input(self) -> None:
        self.length = float(input("length>>"))
        self.theta = float(input("theta>>"))
        self.theta_dot = float(input("theta dot>>"))
        self.dt = float(input("dt>>"))
        self.radius = float(input("radius>>"))
        self.viscosity = float(input("viscosity>>"))

    def process(self, max_time: float) -> Tuple[np.ndarray, np.ndarray]:
        times = []
        thetas = []
        for i in tqdm(np.arange(self.time, max_time, self.dt)):
            times.append(i)
            thetas.append(self.theta)

            self.step()

        return np.array(times), np.array(thetas)

    def step(self):
        mu = 6 * math.pi * self.viscosity * self.radius
        double_dot_theta = (
                -G / self.length * math.sin(math.radians(self.theta))
                - mu * self.theta_dot * self.dt
        )
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

            coord = offset[0] + 500 * math.sin(math.radians(self.theta)), offset[1] + 500 * math.cos(
                math.radians(self.theta))

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
