import os
import sys
sys.path.append(os.pardir)
from modules.ga import uniformcrossover
from modules.fitnessfunction import simple_macd_params


class UniformCrossoverMacd:
    """
    一様交叉を使って、MACDのパラメータを最適化する
    """
    DEFAULT_STEPS = 300

    def __init__(self):
        situation = list()
        situation.append((1, 20))
        situation.append((20, 40))
        situation.append((1, 15))
        candle_type = '15min'
        fitness_function = simple_macd_params.SimpleMacDParams(candle_type)
        self.ga = uniformcrossover.UniformCrossover(situation, fitness_function, population=15,
                                                    mutation=2, cross=50, elite_num=1)

    def __call__(self, steps=DEFAULT_STEPS):
        """
       バックテスト
       :param steps: int 世代交代数
       :return:
       """
        self.ga(steps)
