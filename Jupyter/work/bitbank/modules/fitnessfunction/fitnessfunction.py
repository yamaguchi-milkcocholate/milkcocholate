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

    @abstractmethod
    def calc_fitness(self, geno_type, should_log, population_id):
        pass

    @abstractmethod
    def calc_result(self, **kwargs):
        pass

    @abstractmethod
    def calc_result_and_log(self, population_id, **kwargs):
        pass

    def get_fitness_function_id(self):
        return self._fitness_function_id

    def get_approach(self):
        return self._approach
