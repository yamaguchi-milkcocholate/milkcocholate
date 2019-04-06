from abc import ABC
from abc import abstractmethod
from bitbank.gp.condition import Condition


class FitnessFunction(ABC):

    def __init__(self):
        self.condition = Condition()

    @abstractmethod
    def calc_fitness(self, genomes):
        pass

    def get_condition(self):
        return self.condition
