import os
import sys
import pprint
sys.path.append(os.pardir)
from modules.ga import uniformcrossover
from modules.fitnessfunction import simple_macd_params


class UniformCrossoverMacd:
    """
    一様交叉を使って、MACDのパラメータを最適化する
    """
    DEFAULT_STEPS = 300

    def __init__(self, situation, candle_type, population, mutation, cross, elite_num):
        fitness_function = simple_macd_params.SimpleMacDParams(candle_type)
        self.ga = uniformcrossover.UniformCrossover(situation, fitness_function, population=population,
                                                    mutation=mutation, cross=cross, elite_num=elite_num)

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
