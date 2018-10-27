from abc import ABC, abstractmethod
from modules.datamanager import picker
import numpy as np


class FitnessFunction(ABC):
    BIT_BANK_CANDLE_STICK = ['5min', '15min', '1hour']
    BATCH_INSERT_NUM = 20
    INIT_BIT_COIN_AMOUNT = 1

    def __init__(self, candle_type, db_dept, fitness_function_id):
        if candle_type in self.BIT_BANK_CANDLE_STICK:
            self._candlestick = picker.Picker(candle_type).get_candlestick()
            self._db_dept = db_dept
            self._fitness_function_id = fitness_function_id
            self._approach = None
        else:
            raise TypeError('candle type is not found')

    def calc_fitness(self, geno_type, should_log, population_id):
        """
        calc_resultメソッドより適応度を計算
        :param geno_type      numpy      遺伝子
        :param should_log     bool       記録を取るべきかどうか
        :param population_id  int        テーブル'populations'のid
        :return:              numpy      適応度
        """
        population = geno_type.shape[0]
        fitness_list = list()
        # 1番目のもっとも優れた個体
        genome = geno_type[0]
        data = self._approach(genome=genome)
        if should_log:
            fitness_result = self.calc_result_and_log(data, population_id)
        else:
            fitness_result = self.calc_result(data)
        fitness_list.append(fitness_result)
        # 2番目以降の個体
        for genome_i in range(1, population):
            genome = geno_type(genome_i)
            data = self._approach(genome=genome)
            fitness_list.append(fitness_result)
        del data
        return np.asarray(a=fitness_list, dtype=np.int32)

    @abstractmethod
    def calc_result(self, data):
        pass

    @abstractmethod
    def calc_result_and_log(self, data, population_id):
        pass

    def get_fitness_function_id(self):
        return self._fitness_function_id

    def get_approach(self):
        return self._approach
