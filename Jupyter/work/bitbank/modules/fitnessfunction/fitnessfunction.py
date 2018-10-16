from abc import ABC, abstractmethod
from modules.datamanager import picker


class FitnessFunction(ABC):
    BIT_BANK_CANDLE_STICK = ['5min', '15min', '1hour']

    def __init__(self, candle_type, db_dept):
        if candle_type in self.BIT_BANK_CANDLE_STICK:
            self.candlestick = picker.Picker(candle_type).get_candlestick()
            self.db_dept = db_dept
        else:
            raise TypeError('candle type is not found')

    @abstractmethod
    def calc_fitness(self, geno_type, should_log, population_id):
        pass
