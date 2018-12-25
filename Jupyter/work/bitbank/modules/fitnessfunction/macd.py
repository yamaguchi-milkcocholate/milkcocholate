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
            is_pickle=False
        )
        self.trend_15min = None
        self.trend_5min = None
        self.area_15min = None
        self.area_5min = None
        self.max_histogram_5min = None
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
                if benefit <= self.LOSS_CUT:
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
        return fitness

    def calc_result_and_log(self, population_id, **kwargs):
        return None

    def operation(self, data_i, has_coin, genome):
        histogram_15min = float(self.__data.loc[data_i].histogram_15min)
        histogram_1min = float(self.__data.loc[data_i].histogram_1min)
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
        else:
            self.area_15min = list()
            self.area_15min.append(histogram_15min)
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
            step_size = len(self.area_5min)
            start_decrease = True
        else:
            step_size = None
            start_decrease = False

        if start_decrease:

            # 買い
            if has_coin is False:
                threshold_15min = genome[0]
                threshold_5min = genome[1]
                decrease_rate = genome[2]
                step_rate = genome[3]
                max_step_rate = genome[4]
                # MAX条件
                max_threshold = step_rate * step_size * step_size
                # 降下条件
                decrease_threshold = self.max_histogram_5min * decrease_rate
                factor_3 = self.is_exceed(self.max_histogram_5min, max_threshold)
                factor_4 = self.is_exceed(decrease_threshold, histogram_1min)
                # print(decrease_threshold, histogram_1min)

                if factor_3:
                    self.check[2] += 1
                if factor_4:
                    self.check[3] += 1
                if factor_3 and factor_4:
                    operation = self.BUY
                else:
                    operation = self.STAY
            # 売り
            else:
                threshold_15min = genome[5]
                threshold_5min = genome[6]
                decrease_rate = genome[7]
                step_rate = genome[8]
                max_step_rate = genome[9]
                # MAX条件
                max_threshold = step_rate * step_size * step_size
                # 降下条件
                decrease_threshold = self.max_histogram_5min * decrease_rate
                factor_3 = self.is_exceed(max_threshold, self.max_histogram_5min)
                factor_4 = self.is_exceed(histogram_1min, decrease_threshold)
                """
                print('--')
                print(max_threshold, self.max_histogram_5min)
                print(histogram_1min, decrease_threshold)
                """
                if factor_3 and factor_4:
                    operation = self.SELL
                else:
                    operation = self.STAY
        else:
            operation = self.STAY

        return operation

    def loss_cut(self, fitness, loss_cut, transaction):
        fitness = fitness + 0.5 * fitness * (-math.log(loss_cut + 1, 100) + math.log(transaction + 1, 100)) + self.DEFAULT_YEN_POSITION
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
