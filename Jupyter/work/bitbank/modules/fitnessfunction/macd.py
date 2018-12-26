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
            signal=hyper_params['signal'],
            is_pickle=True
        )
        self.trend_15min = None
        self.trend_5min = None
        self.area_15min = None
        self.area_5min = None
        self.max_histogram_5min = None
        self.max_histogram_15min = None
        self.check = None
        self.check_detail = None

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
        self.trend_15min = self.PLUS
        self.trend_5min = self.PLUS
        self.area_15min = list()
        self.area_5min = list()
        self.max_histogram_5min = 0
        self.max_histogram_15min = 0
        self.check = [0, 0, 0, 0]
        self.check_detail = [0, 0, 0, 0]

        genome = kwargs['genome']
        coin = 0
        has_coin = False
        loss_cut = 0
        fitness = 0
        transaction = 0
        for data_i in range(len(self.__data)):
            price = self.__data.loc[data_i].price

            operation = self.operation(
                data_i=data_i,
                has_coin=has_coin,
                genome=genome,
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
                if benefit <= 0:
                    loss_cut += 1

        benefit = fitness
        fitness = self.loss_cut(fitness=fitness, loss_cut=loss_cut, transaction=transaction)
        print(
            'fitness',
            fitness,
            'loss cut',
            loss_cut,
            'transaction',
            transaction,
            'benefit',
            benefit
        )
        print(self.check)
        print(self.check_detail)
        return fitness

    def calc_result_and_log(self, population_id, **kwargs):
        return None

    def operation(self, data_i, has_coin, genome):
        histogram_15min = float(self.__data.loc[data_i].histogram_15min)
        histogram_1min = float(self.__data.loc[data_i].histogram_5min)
        pre_trend_15min = self.trend_15min
        pre_trend_5min = self.trend_5min
        if histogram_15min >= 0:
            self.trend_15min = self.PLUS
        elif histogram_15min < 0:
            self.trend_15min = self.MINUS
        if histogram_1min >= 0:
            self.trend_5min = self.PLUS
        elif histogram_1min < 0:
            self.trend_5min = self.MINUS

        if pre_trend_15min == self.trend_15min:
            self.area_15min.append(histogram_15min)
            if abs(self.max_histogram_15min) < abs(histogram_15min):
                self.max_histogram_15min = histogram_15min
        else:
            self.area_15min = list()
            self.area_15min.append(histogram_15min)
            self.max_histogram_15min = histogram_15min
        if pre_trend_5min == self.trend_5min:
            self.area_5min.append(histogram_1min)
            if abs(self.max_histogram_5min) < abs(histogram_1min):
                self.max_histogram_5min = histogram_1min
        else:
            self.area_5min = list()
            self.area_5min.append(histogram_1min)
            self.max_histogram_5min = histogram_1min

        # 山が下がり始めたら
        if len(self.area_5min) > 1 and self.is_exceed(abs(self.area_5min[-1]), abs(self.area_5min[-2])):
            step_size_5min = len(self.area_5min)
            start_decrease_5min = True
        else:
            step_size_5min = None
            start_decrease_5min = False
        if len(self.area_15min) > 1 and self.is_exceed(abs(self.area_15min[-1]), abs(self.area_15min[-2])):
            step_size_15min = len(self.area_15min)
            start_decrease_15min = True
        else:
            step_size_15min = None
            start_decrease_15min = False

        if start_decrease_5min and start_decrease_15min:

            # 買い
            if has_coin is False:
                decrease_rate_15min = genome[0]
                step_rate_15min = genome[1]
                decrease_rate_5min = genome[2]
                step_rate_5min = genome[3]
                # MAX条件
                max_threshold_5min = step_rate_5min * step_size_5min * self.max_histogram_5min
                max_threshold_15min = step_rate_15min * step_size_15min * self.max_histogram_15min
                # 降下条件
                decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min
                decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min
                factor_1 = self.is_exceed(self.max_histogram_15min, max_threshold_15min)
                factor_2 = self.is_exceed(decrease_threshold_15min, histogram_15min)
                factor_3 = self.is_exceed(self.max_histogram_5min, max_threshold_5min)
                factor_4 = self.is_exceed(decrease_threshold_5min, histogram_1min)

                if factor_1:
                    self.check[0] += 1
                if factor_2:
                    self.check[1] += 1
                if factor_3:
                    self.check[2] += 1
                if factor_4:
                    self.check[3] += 1

                if factor_1 and factor_2 and factor_3 and factor_4:
                    operation = self.BUY
                else:
                    operation = self.STAY
            # 売り
            else:
                decrease_rate_15min = genome[4]
                step_rate_15min = genome[5]
                decrease_rate_5min = genome[6]
                step_rate_5min = genome[7]
                # MAX条件
                max_threshold_5min = step_rate_5min * step_size_5min * self.max_histogram_5min
                max_threshold_15min = step_rate_15min * step_size_15min * self.max_histogram_15min
                # 降下条件
                decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min
                decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min
                factor_1 = self.is_exceed(max_threshold_15min, self.max_histogram_15min)
                factor_2 = self.is_exceed(histogram_15min, decrease_threshold_15min)
                factor_3 = self.is_exceed(max_threshold_5min, self.max_histogram_5min)
                factor_4 = self.is_exceed(histogram_1min, decrease_threshold_5min)

                if factor_1:
                    self.check_detail[0] += 1
                if factor_2:
                    self.check_detail[1] += 1
                if factor_3:
                    self.check_detail[2] += 1
                if factor_4:
                    self.check_detail[3] += 1

                if factor_1 and factor_2 and factor_3 and factor_4:
                    operation = self.SELL
                else:
                    operation = self.STAY
        else:
            operation = self.STAY

        return operation

    def loss_cut(self, fitness, loss_cut, transaction):
        fitness += self.DEFAULT_YEN_POSITION * (-math.log(loss_cut + 1, 10) + 2 * math.log(transaction + 1, 10))
        if fitness <= 0:
            fitness = 1
        return fitness

    @staticmethod
    def is_exceed(x, y):
        """
        :param x: 小さい
        :param y: 大きい
        :return: bool
        """
        if y > x:
            return True
        else:
            return False
