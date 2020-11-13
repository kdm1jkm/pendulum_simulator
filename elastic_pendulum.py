import numpy as np
import math
from typing import Tuple, List
import matplotlib as mpl
import matplotlib.pylab as plt
from tqdm import tqdm
import sympy

G = 9.8


class elastic_pendulum:
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

    def run_with_input(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        self.get_input()
        t = float(input("time>>"))
        return self.process(t)

    def get_input(self) -> None:
        self.original_length = float(input("Original length>>"))
        self.delta_length = float(input("delta length>>"))
        self.length_dot = float(input("length dot>>"))
        self.theta = float(input("theta>>"))
        self.theta_dot = float(input("theta dot>>"))
        self.mass = float(input("mass>>"))
        self.spring_constant = float(input("spring contant>>"))
        self.dt = float(input("dt>>"))

    def process(self, max_time: float) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        times = []
        thetas = []
        lengths = []
        # pbar = tqdm(total=max_time)
        for _ in tqdm(np.arange(self.time, max_time, self.dt)):
            # while self.time < max_time:
            times.append(self.time)
            thetas.append(self.theta)
            lengths.append(self.length)

            ΔΔθ = (
                -G / self.length * math.sin(math.radians(self.theta))
                - 2 * self.length_dot / self.length * self.theta_dot
            )
            ΔΔlength = (
                self.length * self.theta_dot ** 2
                - self.spring_constant / self.mass * self.delta_length
                + G * math.cos(math.radians(self.theta))
            )

            self.theta_dot += ΔΔθ * self.dt
            self.length_dot += ΔΔlength * self.dt

            self.theta += self.theta_dot * self.dt
            self.delta_length += self.length_dot * self.dt

            self.time += self.dt
            # pbar.total = int(self.time)
            # pbar.update(self.dt)
        return (np.array(times), np.array(thetas), np.array(lengths))

    @property
    def length(self):
        return self.original_length + self.delta_length


if __name__ == "__main__":
    obj = elastic_pendulum()
    times, thetas, lengths = obj.run_with_input()
    plt.figure(1)
    plt.title("thetas")
    plt.plot(times, thetas)
    plt.figure(2)
    plt.title("lengths")
    plt.plot(times, lengths)
    plt.show()
