import os
import sys
import pprint
sys.path.append(os.pardir)
from modules.ga import sga
from modules.fitnessfunction import simple_macd_params


class SgaMacd:
    """
    SGAを使って、MACDのパラメータを最適化する
    """
    DEFAULT_STEPS = 300

    def __init__(self, situation, candle_type, population, mutation, cross, elite_num):
        fitness_function = simple_macd_params.SimpleMacDParams(candle_type)
        self.ga = sga.SimpleGeneticAlgorithm(situation=situation, population=population,
                                             fitness_function=fitness_function, mutation=mutation,
                                             cross=cross, elite_num=elite_num)

    def __call__(self, steps=DEFAULT_STEPS):
        """
        バックテスト
        :param steps: int 世代交代数
        :return:
        """
        self.ga(steps)
        print('geno_type')
        pprint.pprint(self.ga.geno_type)
        print('fitness')
        pprint.pprint(self.ga.fitness)
