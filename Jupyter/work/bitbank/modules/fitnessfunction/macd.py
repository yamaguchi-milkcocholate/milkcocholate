import numpy as np
import math
from modules.datamanager.macd import MACD
from modules.fitnessfunction.fitnessfunction import FitnessFunction


class MACD_(FitnessFunction):
    FITNESS_FUNCTION_ID = 6
    DEFAULT_YEN_POSITION = 1000
    LOSS_CUT = 1000
    MINUS = -1
    PLUS = 1

    BUY = 1
    SELL = 2
    STAY = 3

    """
    MACDシグナルから取引をする
    """

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
        # MACDアプローチ
        self._approach = MACD()
        self.__data = self._approach(
            short_term=hyper_params['short_term'],
            long_term=hyper_params['long_term'],
            signal=hyper_params['signal']
        )

    def calc_fitness(self, geno_type, should_log, population_id):
        """
        適応度を計算
        :param geno_type:
        :param should_log:
        :param population_id:
        :return: numpy
        """
        fitness_list = list()
        for geno_i in range(len(geno_type)):
            genome = geno_type[geno_i]
            fitness_result = self.calc_result(genome=genome)
            fitness_list.append(fitness_result)
        return np.asarray(a=fitness_list)

    def calc_result(self, **kwargs):
        genome = kwargs['genome']
        coin = 0
        benefit = 0
        has_coin = False
        loss_cut = 0
        fitness = 0
        transaction = 0
        trend_15min = 1
        trend_5min = 1
        area_15min = [0]
        area_5min = [0]
        max_histogram_5min = 0
        for data_i in range(len(self.__data)):
            price = self.__data.loc[data_i].price

            operation, trend_15min, trend_5min, area_15min, area_5min, max_histogram_5min = self.operation(
                data_i=data_i,
                has_coin=has_coin,
                genome=genome,
                trend_15min=trend_15min,
                trend_5min=trend_5min,
                area_15min=area_15min,
                area_5min=area_5min,
                max_histogram_5min=max_histogram_5min
            )

            if self.BUY == operation:
                coin = self.DEFAULT_YEN_POSITION / price
                has_coin = True
            elif self.SELL == operation:
                benefit = price * coin - self.DEFAULT_YEN_POSITION
                coin = 0
                has_coin = False
                fitness += benefit
                transaction += 1

            # 損切り
            if benefit <= self.LOSS_CUT:
                loss_cut += 1

        fitness = self.loss_cut(fitness=fitness, loss_cut=loss_cut, transaction=transaction)
        print(
            'fitness',
            fitness,
            'loss cut',
            loss_cut,
            'transaction',
            transaction
        )
        return fitness

    def calc_result_and_log(self, population_id, **kwargs):
        return None

    def operation(self, data_i, has_coin,
                  genome, trend_15min, trend_5min, area_15min, area_5min, max_histogram_5min
                  ):
        histogram_15min = self.__data.loc[data_i].histogram_15min
        histogram_5min = self.__data.loc[data_i].histogram_5min
        histogram_1min = self.__data.loc[data_i].histogram_1min
        pre_trend_15min = trend_15min
        pre_trend_5min = trend_5min
        if histogram_15min >= 0:
            trend_15min = self.PLUS
        elif histogram_15min < 0:
            trend_15min = self.MINUS
        if histogram_1min >= 0:
            trend_5min = self.PLUS
        elif histogram_1min < 0:
            trend_5min = self.MINUS

        if pre_trend_15min == trend_15min:
            area_15min.append(histogram_15min)
        else:
            area_15min = [histogram_15min]
        if pre_trend_5min == trend_5min:
            area_5min.append(histogram_5min)
            if abs(max_histogram_5min) < abs(histogram_5min):
                max_histogram_5min = histogram_5min
        else:
            area_5min = [histogram_5min]
            max_histogram_5min = histogram_5min

        # 買い
        if has_coin is False:
            threshold_15min = genome[0]
            threshold_5min = genome[1]
            max_histogram = genome[2]
            decrease_rate = genome[3]
            ave_15min = sum(area_15min) / len(area_15min)
            ave_5min = sum(area_5min) / len(area_5min)
            factor_1 = self.is_exceed(threshold_15min, ave_15min)
            factor_2 = self.is_exceed(threshold_5min, ave_5min)
            factor_3 = self.is_exceed(max_histogram, max_histogram_5min)
            factor_4 = self.is_exceed(histogram_1min, decrease_rate * max_histogram)
            if factor_1 and factor_2 and factor_3 and factor_4:
                operation = self.BUY
            else:
                operation = self.STAY
        # 売り
        else:
            threshold_15min = genome[4]
            threshold_5min = genome[5]
            max_histogram = genome[6]
            decrease_rate = genome[7]
            ave_15min = sum(area_15min) / len(area_15min)
            ave_5min = sum(area_5min) / len(area_5min)
            factor_1 = self.is_exceed(threshold_15min, ave_15min)
            factor_2 = self.is_exceed(threshold_5min, ave_5min)
            factor_3 = self.is_exceed(max_histogram, max_histogram_5min)
            factor_4 = self.is_exceed(histogram_1min, decrease_rate * max_histogram)
            if factor_1 and factor_2 and factor_3 and factor_4:
                operation = self.SELL
            else:
                operation = self.STAY

        return operation, trend_15min, trend_5min, area_15min, area_5min, max_histogram_5min

    @staticmethod
    def loss_cut(fitness, loss_cut, transaction):
        fitness = fitness + 0.5 * fitness * (-math.log(loss_cut + 1, 10) + math.log(transaction + 1, 100))
        if fitness <= 0:
            fitness = 1
        return fitness

    @staticmethod
    def is_exceed(x, y):
        """
        :param x: 小さい
        :param y: 大きい
        :return:
        """
        x = abs(x)
        y = abs(y)
        if y > x:
            return True
        else:
            return False
