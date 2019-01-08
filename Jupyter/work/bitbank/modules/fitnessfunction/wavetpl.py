from modules.gp.functions import *
from modules.fitnessfunction.fitnessfunction import FitnessFunction
from modules.datamanager.wavetpl import WaveTemplateData
import numpy as np


class WaveTemplate(FitnessFunction):
    FITNESS_FUNCTION_ID = 6

    """
    波形テンプレート解析
    1. 価格
    2. 短期単純移動平均線
    3. 長期単純移動平均線
    4. 平滑移動平均線
    """

    def __init__(self, candle_type, db_dept, hyper_params, coin):
        """
        :param candle_type:  string
        :param db_dept:      object
        :param hyper_params: dict
        :param coin:         string
        """
        super().__init__(
            candle_type=candle_type,
            db_dept=db_dept,
            fitness_function_id=self.FITNESS_FUNCTION_ID,
            coin=coin
        )
        # DataFrameでデータを取り出す(Todo:5minを1minで圧縮して使う)
        self.__approach = WaveTemplateData()
        self._candlestick = self.__approach()

    def calc_fitness(self, geno_type, should_log, population_id):
        """
        適応度を計算
        :param geno_type:      numpy
        :param should_log:     bool
        :param population_id:  int
        :return:               numpy
        """
        population = geno_type.shape[0]
        fitness_list = list()
        # 1番目のもっとも優れた個体
        genome = geno_type[0]
        if should_log:
            # FitnessFunctionの抽象クラス制約で冗長な引数
            fitness_result = self.calc_result_and_log(
                population_id=population_id,
                genome=genome
            )
        else:
            # FitnessFunctionの抽象クラス制約で冗長な引数
            fitness_result = self.calc_result(genome=genome)
        fitness_list.append(fitness_result)
        # 2番目以降の個体
        for genome_i in range(1, population):
            genome = geno_type[genome_i]
            fitness_result = self.calc_result(genome=genome)
            fitness_list.append(fitness_result)
        return np.asarray(a=fitness_list)

    def calc_result(self, **kwargs):
        pass

    def calc_result_and_log(self, population_id, **kwargs):
        pass
