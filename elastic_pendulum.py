import math

import matplotlib.pylab as plt
import numpy as np
from tqdm import tqdm
import pygame
import sys

w, h = 1024, 768
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LT_BLUE = (230, 230, 255)
offset = (w // 2, h // 4)

G = 9.8


class ElasticPendulum:
    def __init__(self):
        self.original_length: float = 1
        self.delta_length: float = 0
        self.length_dot: float = 0
        self.theta: float = 60
        self.theta_dot: float = 0
        self.mass: float = 0.1
        self.spring_constant: float = 10
        self.time: float = 0
        self.dt: float = 0.01

    def run_with_input(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        self.get_input()
        t = float(input("time>>"))
        time, theta, length = self.process(t)
        plt.figure(1)
        plt.title("thetas")
        plt.plot(time, theta)

        plt.figure(2)
        plt.title("lengths")
        plt.plot(time, length)

        x = length * np.sin(theta)
        y = -(length * np.cos(theta))

        plt.figure(3)
        plt.title("x, y")
        plt.plot(x, y)

        plt.figure(4)
        plt.gca(projection="3d")
        plt.title("x, y, time")
        plt.plot(x, time, y)
        plt.show()
        return time, theta, length

    def get_input(self) -> None:
        self.original_length = float(input("Original length>>"))
        self.delta_length = float(input("delta length>>"))
        self.length_dot = float(input("length dot>>"))
        self.theta = math.radians(float(input("theta>>")))
        self.theta_dot = math.radians(float(input("theta dot>>")))
        self.mass = float(input("mass>>"))
        self.spring_constant = float(input("spring constant>>"))
        self.dt = float(input("dt>>"))

    def process(self, max_time: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        times = []
        thetas = []
        lengths = []
        for i in tqdm(np.arange(self.time, max_time, self.dt)):
            times.append(i)
            thetas.append(self.theta)
            lengths.append(self.length)

            self.RK4_step()

        self.time = max_time

        return np.array(times), np.array(thetas), np.array(lengths)

    def differentiate(self, info):
        theta_dot, length_dot, theta, delta_length = info[0], info[1], info[2], info[3]
        length = self.original_length + delta_length

        length_double_dot = (length * theta_dot ** 2
                             - self.spring_constant / self.mass * delta_length
                             + G * math.cos(theta))
        theta_double_dot = (-2.0 / length * length_dot * theta_dot
                            - G / length * math.sin(theta))
        return np.array([theta_double_dot, length_double_dot, theta_dot, length_dot])

    def RK4_step(self):
        info = np.array([self.theta_dot, self.length_dot, self.theta, self.delta_length])
        k1 = self.differentiate(info)
        k2 = self.differentiate(info + k1 * self.dt / 2)
        k3 = self.differentiate(info + k2 * self.dt / 2)
        k4 = self.differentiate(info + k3 * self.dt)
        result = (k1 + 2 * k2 + 2 * k3 + k4) / 6 * self.dt

        self.theta_dot += result[0]
        self.length_dot += result[1]
        self.theta += result[2]
        self.delta_length += result[3]

    @property
    def length(self):
        return self.original_length + self.delta_length

    def simulate_with_input(self) -> None:
        self.get_input()
        self.simulate()

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

            coord = (offset[0] + 100 * math.sin(self.theta) * (self.length / self.original_length),
                     offset[1] + 100 * math.cos(self.theta) * (self.length / self.original_length))

            screen.fill(WHITE)
            pygame.draw.circle(screen, BLACK, offset, 8)
            pygame.draw.circle(screen, BLUE, coord, 10)
            pygame.draw.line(screen, RED, offset, coord)

            pygame.display.flip()

            self.RK4_step()


if __name__ == "__main__":
    obj = ElasticPendulum()
    obj.simulate_with_input()
    # time, theta, length = obj.run_with_input()
    # plt.figure(1)
    # plt.title("thetas")
    # plt.plot(time, theta)
    # plt.figure(2)
    # plt.title("lengths")
    # plt.plot(time, length)
    #
    # fig = plt.figure(3)
    # ax = fig.gca(projection='3d')
    # x = length * np.sin(theta)
    # y = -(length * np.cos(theta))
    # ax.plot(x, time, y, label="x, y")
    # ax.legend()
    # plt.show()
