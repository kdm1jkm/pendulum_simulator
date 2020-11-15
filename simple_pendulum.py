import math
import sys
from typing import Tuple

import numpy as np
import pygame
from tqdm import tqdm

G = 9.8
myfont = pygame.font.SysFont('Comic Sans MS', 38)
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

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            x, y = self.length * math.sin(math.radians(self.theta)), self.length * math.sin(math.radians(self.theta))

            screen.fill(WHITE)
            pygame.draw.circle(screen, BLACK, offset, 8)
            pygame.draw.circle(screen, BLUE, (x, y), 10)

            time_string = 'Time: {} seconds'.format(round(self.time, 1))
            text = myfont.render(time_string, False, (0, 0, 0))
            screen.blit(text, (10, 10))

            self.step()
            clock.tick(int(1 / self.dt))
            pygame.display.update()


if __name__ == "__main__":
    obj = SimplePendulum()
    obj.simulate_with_input()
