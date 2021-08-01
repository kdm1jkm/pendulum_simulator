from abc import ABCMeta, abstractmethod


class PendulumSimulator(metaclass=ABCMeta):
    @abstractmethod
    def run_with_input(self):
        pass

    @abstractmethod
    def simulate_with_input(self):
        pass
