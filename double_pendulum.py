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


class DoublePendulum:
    def __init__(self):
        self.length1: float = 2
        self.length2: float = 1
        self.theta1: float = 60
        self.theta2: float = 0
        self.theta_dot1: float = 0
        self.theta_dot2: float = 0
        self.mass1: float = 0.1
        self.mass2: float = 0.2
        self.dt: float = 0.01
        self.time: float = 0

    def run_with_input(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        self.get_input()
        t = float(input("time>>"))
        time, theta1, theta2 = self.process(t)
        plt.figure(1)
        plt.title("thetas")
        plt.plot(time, theta1)
        plt.plot(time, theta2)

        x1 = self.length1 * np.sin(theta1)
        y1 = -(self.length1 * np.cos(theta1))

        x2 = self.length2 * np.sin(theta2) + x1
        y2 = -(self.length2 * np.cos(theta2)) + y1

        plt.figure(3)
        plt.title("x, y")
        plt.plot(x1, y1)
        plt.plot(x2, y2)

        plt.figure(4)
        plt.gca(projection="3d")
        plt.title("x, y, time")
        plt.plot(x1, time, y1)
        plt.plot(x2, time, y2)
        plt.show()
        return time, theta1, theta2

    def get_input(self) -> None:
        self.length1 = float(input("length1>>"))
        self.theta1 = float(input("theta1>>"))
        self.theta_dot1 = float(input("theta_dot1>>"))
        self.mass1 = float(input("mass1>>"))

        self.length2 = float(input("length2>>"))
        self.theta2 = float(input("theta2>>"))
        self.theta_dot2 = float(input("theta_dot2>>"))
        self.mass2 = float(input("mass2>>"))

        self.dt = float(input("dt>>"))

    def process(self, max_time: float) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        times = []
        thetas1 = []
        thetas2 = []
        for i in tqdm(np.arange(self.time, max_time, self.dt)):
            times.append(i)
            thetas1.append(self.theta1)
            thetas2.append(self.theta2)

            self.RK4_step()

        self.time = max_time

        return np.array(times), np.array(thetas1), np.array(thetas2)

    def differentiate(self, info):
        theta_dot1, theta_dot2, theta1, theta2 = info[0], info[1], info[2], info[3]

        m = np.array([[(self.mass1 + self.mass2) * self.length1, self.mass2 * self.length2 * math.cos(theta1 - theta2)],
                      [self.length1 * math.cos(theta1 - theta2), self.length2]])
        f = np.array([-self.mass2 * self.length2 * theta_dot2 * math.sin(theta1 - theta2) - (
                self.mass1 + self.mass2) * G * math.sin(theta1),
                      self.length1 * (theta_dot1 ** 2) * math.sin(theta1 - theta2) - G * math.sin(theta2)])
        theta_double_dot1, theta_double_dot2 = np.linalg.inv(m).dot(f)
        return np.array([theta_double_dot1, theta_double_dot2, theta_dot1, theta_dot2])

    def RK4_step(self):
        info = np.array([self.theta_dot1, self.theta_dot2, self.theta1, self.theta2])
        k1 = self.differentiate(info)
        k2 = self.differentiate(info + k1 * self.dt / 2)
        k3 = self.differentiate(info + k2 * self.dt / 2)
        k4 = self.differentiate(info + k3 * self.dt)
        result = (k1 + 2 * k2 + 2 * k3 + k4) / 6

        self.theta_dot1 += result[0]*self.dt
        self.theta_dot2 += result[1]*self.dt
        self.theta1 += result[2]*self.dt
        self.theta2 += result[3]*self.dt

        return result

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

            coord1 = (offset[0] + 300 * math.sin(self.theta1) * (self.length1 / (self.length1 + self.length2)),
                      offset[1] + 300 * math.cos(self.theta1) * (self.length1 / (self.length1 + self.length2)))
            coord2 = (coord1[0] + 300 * math.sin(self.theta2) * (self.length2 / (self.length1 + self.length2)),
                      coord1[1] + 300 * math.cos(self.theta2) * (self.length2 / (self.length1 + self.length2)))

            result = self.RK4_step()

            screen.fill(WHITE)
            pygame.draw.circle(screen, BLACK, offset, 8)
            pygame.draw.circle(screen, BLUE, coord1, 10)
            pygame.draw.line(screen, RED, offset, coord1)
            pygame.draw.circle(screen, BLUE, coord2, 10)
            pygame.draw.line(screen, RED, coord1, coord2)

            pygame.draw.line(screen, BLUE, coord1, np.array(coord1) + result[0]*10)
            pygame.draw.line(screen, BLUE, coord2, np.array(coord2) + result[1]*10)
            pygame.draw.line(screen, RED, coord1, np.array(coord1) + result[2]*10)
            pygame.draw.line(screen, RED, coord2, np.array(coord2) + result[3]*10)

            pygame.display.flip()



if __name__ == "__main__":
    obj = DoublePendulum()
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
