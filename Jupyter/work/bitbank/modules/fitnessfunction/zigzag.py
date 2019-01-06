import numpy as np
from modules.fitnessfunction.fitnessfunction import FitnessFunction
from modules.datamanager.zigzag import ZigZag


class ZigZagFunction(FitnessFunction):
    FITNESS_FUNCTION_ID = 7

    BUY = 1
    STAY = 2
    SELL = 3

    def __init__(self, candle_type, db_dept, hyper_params, coin):
        """
        :param candle_type:
        :param db_dept:
        :param hyper_params:
        :param coin:
        """
        super().__init__(
            candle_type=candle_type,
            db_dept=db_dept,
            fitness_function_id=self.FITNESS_FUNCTION_ID,
            coin=coin
        )
        zigzag = ZigZag()
        self.__data = zigzag.get_candlestick()

    def calc_fitness(self, geno_type, should_log, population_id):
        pass

    def calc_result(self, **kwargs):
        pass

    def calc_result_and_log(self, population_id, **kwargs):
        pass
