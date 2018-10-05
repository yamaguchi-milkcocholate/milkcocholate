# coding:utf-8
from modules.ga import sga
from modules.fitnessfunction import simple_macd_params


class SgaMacd:
    """
    SGAを使って、MACDのパラメータを最適化する
    """
    DEFAULT_STEPS = 300

    def __init__(self):
        situation = list()
        situation.append((1, 50))
        situation.append((2, 100))
        situation.append((1, 50))
        candle_type = '1hour'
        fitness_function = simple_macd_params.SimpleMacDParams(candle_type)
        self.ga = sga.SimpleGeneticAlgorithm(situation, population=11, fitness_function=fitness_function)

    def back_test(self, steps=DEFAULT_STEPS):
        """
        バックテスト
        :param steps: int 世代交代数
        :return:
        """
        self.ga(steps)

    def processing(self):
        """
        スケジューラによる実行処理
        :return:
        """
        pass


if __name__ == '__main__':
    sga_macd = SgaMacd()
    sga_macd.back_test(1000)
    print(sga_macd.ga.geno_type)
    print(sga_macd.ga.fitness)

