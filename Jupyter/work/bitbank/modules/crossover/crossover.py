from abc import ABC, abstractmethod
import numpy as np


class Crossover(ABC):

    def __init__(self, crossover_id):
        self._cross_over_id = crossover_id

    @classmethod
    @abstractmethod
    def determine_next_generation(cls, geno_type, fitness, situation, mutation, cross, elite_num):
        pass

    @staticmethod
    def select_elites(elite_num, geno_type, fitness):
        """
        エリート個体の遺伝子を返す
        :param elite_num    int   エリートの個体数
        :param fitness:     numpy 適応度
        :param geno_type    numpy 遺伝子
        :return:            numpy エリート個体の遺伝子
        """
        fitness = np.argsort(fitness)[::-1]
        elites = geno_type[fitness[elite_num]]
        return elites

    def get_crossover_id(self):
        return self._cross_over_id
