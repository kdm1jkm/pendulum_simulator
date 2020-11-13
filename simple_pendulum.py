import math
import numpy as np
from typing import Tuple, List
import matplotlib as mpl
import matplotlib.pylab as plt
from tqdm import tqdm
import pygame
from pygame.locals import *

G = 9.8


class simple_pendulum:
    def __init__(self):
        self.length: float = 1
        self.theta: float = 60
        self.theta_dot: float = 0
        self.dt: float = 0.01
        self.radius: float = 0.01
        self.viscosity: float = 0.0000174
        self.time: float = 0

    def run_with_input(self) -> Tuple[np.ndarray, np.ndarray]:
        self.get_input()
        t = float(input("time>>"))
        return self.process(t)

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

        return (np.array(times), np.array(thetas))

    def step(self):
        mu = 6 * math.pi * self.viscosity * self.radius
        ΔΔθ = (
            -G / self.length * math.sin(math.radians(self.theta))
            - mu * self.theta_dot * self.dt
        )
        self.theta_dot += ΔΔθ * self.dt
        self.theta += self.theta_dot * self.dt

    def simulate(self):
        pygame.init()
        screen = pygame.display.set_mode([700, 500])
        clock = pygame.time.Clock()


if __name__ == "__main__":
    obj = simple_pendulum()
    times, thetas = obj.run_with_input()

    plt.figure(1)
    plt.title("thetas")
    plt.plot(times, thetas)
    plt.show()
