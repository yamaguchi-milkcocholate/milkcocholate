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
        self.start_macd_15min = None
        self.start_macd_5min = None
        self.start_signal_15min = None
        self.start_signal_5min = None
        self.start_decrease_15min = None
        self.start_decrease_5min = None
        self.mount_15min = None
        self.mount_5min = None
        self.buying_price = None
        self.max_price = None
        self.is_plus_start_15min = None
        self.is_plus_start_5min = None
        self.check = None
        self.check_detail = None
        self.check_ave = None

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
        self.start_macd_15min = 0
        self.start_macd_5min = 0
        self.start_signal_15min = 0
        self.start_signal_5min = 0
        self.start_decrease_15min = False
        self.start_decrease_5min = False
        self.mount_15min = 1
        self.mount_5min = 1
        self.is_plus_start_15min = False
        self.is_plus_start_5min = False
        self.check = [0, 0]
        self.check_detail = [0, 0]

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
                self.buying_price = price
            elif self.SELL == operation:
                benefit = price * coin - self.DEFAULT_YEN_POSITION
                coin = 0
                has_coin = False
                fitness += benefit
                transaction += 1
                self.buying_price = None
                # 損切り
                if benefit <= 0:
                    loss_cut += 1
                    self.check_detail[1] += benefit
                else:
                    self.check_detail[0] += benefit

        benefit = fitness
        fitness = self.loss_cut(fitness=fitness, loss_cut=loss_cut, transaction=transaction)
        if transaction > 0:
            success = round(100 * (transaction - loss_cut) / transaction)
        else:
            success = 0
        print(
            'fitness',
            fitness,
            'loss cut',
            loss_cut,
            'transaction',
            transaction,
            'benefit',
            benefit,
            self.check,
            self.check_detail,
            success
        )
        return fitness

    def calc_result_and_log(self, population_id, **kwargs):
        return None

    @staticmethod
    def loss_cut(fitness, loss_cut, transaction):
        if fitness <= 0:
            fitness = 1
        else:
            fitness = fitness - 1 * fitness * math.sqrt((loss_cut + 1) / transaction)
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

    @staticmethod
    def and_gate(*args):
        return all(args)

    def operation(self, data_i, has_coin, genome):
        histogram_15min = float(self.__data.loc[data_i].histogram_15min)
        histogram_1min = float(self.__data.loc[data_i].histogram_5min)
        pre_trend_15min = self.trend_15min
        pre_trend_5min = self.trend_5min
        macd_15min = float(self.__data.loc[data_i].macd_15min)
        macd_5min = float(self.__data.loc[data_i].macd_5min)
        signal_15min = float(self.__data.loc[data_i].signal_15min)
        signal_5min = float(self.__data.loc[data_i].signal_5min)
        price = float(self.__data.loc[data_i].price)
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
            self.start_macd_15min = macd_15min
            self.start_signal_15min = signal_15min
            if has_coin is False and signal_15min > 0:
                self.is_plus_start_15min = True
            else:
                self.is_plus_start_15min = False
        if pre_trend_5min == self.trend_5min:
            self.area_5min.append(histogram_1min)
            if abs(self.max_histogram_5min) < abs(histogram_1min):
                self.max_histogram_5min = histogram_1min
        else:
            self.area_5min = list()
            self.area_5min.append(histogram_1min)
            self.max_histogram_5min = histogram_1min
            self.start_macd_5min = macd_5min
            self.start_signal_5min = signal_5min
            if has_coin is False and signal_5min > 0:
                self.is_plus_start_5min = True
            else:
                self.is_plus_start_5min = False

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
            if has_coin is False and self.is_plus_start_15min and self.is_plus_start_5min:
                decrease_rate_15min = genome[0]
                step_rate_15min = genome[1]
                decrease_rate_5min = genome[2]
                step_rate_5min = genome[3]
                start_macd_15min = genome[4]
                start_signal_15min = genome[5]
                start_macd_5min = genome[6]
                start_signal_5min = genome[7]
                end_macd_15min = genome[8]
                end_signal_15min = genome[9]
                end_macd_5min = genome[10]
                end_signal_5min = genome[11]
                # MAX条件
                max_threshold_5min = step_rate_5min * step_size_5min * self.max_histogram_5min
                max_threshold_5min += start_macd_5min * self.start_macd_5min
                max_threshold_5min += start_signal_5min * self.start_signal_5min
                max_threshold_5min += end_macd_5min * macd_5min
                max_threshold_5min += end_signal_5min * signal_5min
                max_threshold_15min = step_rate_15min * step_size_5min * self.max_histogram_15min
                max_threshold_15min += start_macd_15min * self.start_macd_15min
                max_threshold_15min += start_signal_15min * self.start_signal_15min
                max_threshold_15min += end_macd_15min * macd_15min
                max_threshold_15min += end_signal_15min * signal_15min
                # 降下条件
                decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min
                decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min

                buy = self.and_gate(
                    self.is_exceed(self.max_histogram_15min, max_threshold_15min),
                    self.is_exceed(decrease_threshold_15min, histogram_15min),
                    self.is_exceed(self.max_histogram_5min, max_threshold_5min),
                    self.is_exceed(decrease_threshold_5min, histogram_1min),
                )
                if buy:
                    operation = self.BUY
                else:
                    operation = self.STAY
            # 売り
            elif has_coin is True:
                decrease_rate_15min = genome[12]
                step_rate_15min = genome[13]
                decrease_rate_5min = genome[14]
                step_rate_5min = genome[15]
                start_macd_5min = genome[16]
                start_signal_5min = genome[17]
                start_macd_15min = genome[18]
                start_signal_15min = genome[19]
                end_macd_5min = genome[16]
                end_signal_5min = genome[17]
                end_macd_15min = genome[18]
                end_signal_15min = genome[19]
                price_rate = genome[28]
                # MAX条件
                max_threshold_5min = step_rate_5min * step_size_5min * self.max_histogram_5min
                max_threshold_5min += start_macd_5min * self.start_macd_5min
                max_threshold_5min += start_signal_5min * self.start_signal_5min
                max_threshold_5min += end_macd_5min * macd_5min
                max_threshold_5min += end_signal_5min * signal_5min
                max_threshold_15min = step_rate_15min * step_size_15min * self.max_histogram_15min
                max_threshold_15min += start_macd_15min * self.start_macd_15min
                max_threshold_15min += start_signal_15min * self.start_signal_15min
                max_threshold_15min += end_macd_15min * macd_15min
                max_threshold_15min += end_signal_15min * signal_15min
                # 降下条件
                decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min
                decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min

                if not self.max_price:
                    self.max_price = price
                else:
                    if self.max_price < price:
                        self.max_price = price

                sell = self.and_gate(
                    self.is_exceed(max_threshold_15min, self.max_histogram_15min),
                    self.is_exceed(histogram_15min, decrease_threshold_15min),
                    self.is_exceed(max_threshold_5min, self.max_histogram_5min),
                    self.is_exceed(histogram_1min, decrease_threshold_5min),
                )

                if self.max_price * price_rate > price:
                    self.check[1] += 1
                    sell_price = True
                else:
                    sell_price = False

                if sell:
                    self.check[0] += 1

                if sell or sell_price:
                    operation = self.SELL
                else:
                    operation = self.STAY
            else:
                operation = self.STAY
        else:
            operation = self.STAY

        return operation

    def operation_5min(self, data_i, has_coin, genome):
        histogram_5min = float(self.__data.loc[data_i].histogram_5min)
        pre_trend_5min = self.trend_5min
        macd_5min = float(self.__data.loc[data_i].macd_5min)
        signal_5min = float(self.__data.loc[data_i].signal_5min)
        price = float(self.__data.loc[data_i].price)
        if histogram_5min >= 0:
            self.trend_5min = self.PLUS
        elif histogram_5min < 0:
            self.trend_5min = self.MINUS

        if pre_trend_5min == self.trend_5min:
            self.area_5min.append(histogram_5min)
            if abs(self.max_histogram_5min) < abs(histogram_5min):
                self.max_histogram_5min = histogram_5min
        else:
            self.area_5min = list()
            self.area_5min.append(histogram_5min)
            self.max_histogram_5min = histogram_5min
            self.start_macd_5min = macd_5min
            self.start_signal_5min = signal_5min
            self.mount_5min = 1

        if len(self.area_5min) > 1 and self.is_exceed(abs(self.area_5min[-1]),
                                                       abs(self.area_5min[-2])) and not self.start_decrease_5min:
            self.start_decrease_5min = True
            self.mount_5min += 1
        else:
            self.start_decrease_5min = False

        # 買い
        step_size_5min = len(self.area_5min)
        if has_coin is False:
            decrease_rate_5min = genome[2]
            step_rate_5min = genome[3]
            start_macd_5min = genome[6]
            start_signal_5min = genome[7]
            end_macd_5min = genome[10]
            end_signal_5min = genome[11]
            mount_5min = genome[26]
            # MAX条件
            max_threshold_5min = step_rate_5min * step_size_5min * self.max_histogram_5min
            max_threshold_5min /= self.mount_5min / mount_5min
            max_threshold_5min += start_macd_5min * self.start_macd_5min
            max_threshold_5min += start_signal_5min * self.start_signal_5min
            max_threshold_5min += end_macd_5min * macd_5min
            max_threshold_5min += end_signal_5min * signal_5min
            # 降下条件
            decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min

            buy = self.and_gate(
                self.is_exceed(self.max_histogram_5min, max_threshold_5min),
                self.is_exceed(decrease_threshold_5min, histogram_5min),
            )
            if buy:
                operation = self.BUY
            else:
                operation = self.STAY
        # 売り
        elif has_coin is True:
            decrease_rate_5min = genome[14]
            step_rate_5min = genome[15]
            start_macd_5min = genome[18]
            start_signal_5min = genome[19]
            end_macd_5min = genome[22]
            end_signal_5min = genome[23]
            mount_5min = genome[27]
            price_rate = genome[28]
            # MAX条件
            max_threshold_5min = step_rate_5min * step_size_5min * self.max_histogram_5min
            max_threshold_5min /= self.mount_5min / mount_5min
            max_threshold_5min += start_macd_5min * self.start_macd_5min
            max_threshold_5min += start_signal_5min * self.start_signal_5min
            max_threshold_5min += end_macd_5min * macd_5min
            max_threshold_5min += end_signal_5min * signal_5min
            # 降下条件
            decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min

            if not self.max_price:
                self.max_price = price
            else:
                if self.max_price < price:
                    self.max_price = price

            sell = self.and_gate(
                self.is_exceed(max_threshold_5min, self.max_histogram_5min),
                self.is_exceed(histogram_5min, decrease_threshold_5min),
            )

            if self.max_price * price_rate > price:
                self.check[1] += 1
                sell_price = True
            else:
                sell_price = False

            if sell:
                self.check[0] += 1

            if sell or sell_price:
                operation = self.SELL
            else:
                operation = self.STAY
        else:
            operation = self.STAY

        return operation

    def operation_15min(self, data_i, has_coin, genome):
        histogram_15min = float(self.__data.loc[data_i].histogram_15min)
        pre_trend_15min = self.trend_15min
        macd_15min = float(self.__data.loc[data_i].macd_15min)
        signal_15min = float(self.__data.loc[data_i].signal_15min)
        if histogram_15min >= 0:
            self.trend_15min = self.PLUS
        elif histogram_15min < 0:
            self.trend_15min = self.MINUS

        if pre_trend_15min == self.trend_15min:
            self.area_15min.append(histogram_15min)
            if abs(self.max_histogram_15min) < abs(histogram_15min):
                self.max_histogram_15min = histogram_15min
        else:
            self.area_15min = list()
            self.area_15min.append(histogram_15min)
            self.max_histogram_15min = histogram_15min
            self.start_macd_15min = macd_15min
            self.start_signal_15min = signal_15min
            self.mount_15min = 1

        if len(self.area_15min) > 1 and self.is_exceed(abs(self.area_15min[-1]), abs(self.area_15min[-2])) and not self.start_decrease_15min:
            self.start_decrease_15min = True
            self.mount_15min += 1
        else:
            self.start_decrease_15min = False

        # 買い
        step_size_15min = len(self.area_15min)
        if has_coin is False:
            decrease_rate_15min = genome[0]
            step_rate_15min = genome[1]
            start_macd_15min = genome[4]
            start_signal_15min = genome[5]
            end_macd_15min = genome[8]
            end_signal_15min = genome[9]
            mount_15min = genome[24]
            # MAX条件
            max_threshold_15min = step_rate_15min * step_size_15min * self.max_histogram_15min
            max_threshold_15min /= self.mount_15min / mount_15min
            max_threshold_15min += start_macd_15min * self.start_macd_15min
            max_threshold_15min += start_signal_15min * self.start_signal_15min
            max_threshold_15min += end_macd_15min * macd_15min
            max_threshold_15min += end_signal_15min * signal_15min
            # 降下条件
            decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min

            buy = self.and_gate(
                self.is_exceed(self.max_histogram_15min, max_threshold_15min),
                self.is_exceed(decrease_threshold_15min, histogram_15min),
            )
            if buy:
                operation = self.BUY
            else:
                operation = self.STAY
        # 売り
        elif has_coin is True:
            decrease_rate_15min = genome[12]
            step_rate_15min = genome[13]
            start_macd_15min = genome[16]
            start_signal_15min = genome[17]
            end_macd_15min = genome[20]
            end_signal_15min = genome[21]
            mount_15min = genome[25]
            # MAX条件
            max_threshold_15min = step_rate_15min * step_size_15min * self.max_histogram_15min
            max_threshold_15min /= self.mount_15min / mount_15min
            max_threshold_15min += start_macd_15min * self.start_macd_15min
            max_threshold_15min += start_signal_15min * self.start_signal_15min
            max_threshold_15min += end_macd_15min * macd_15min
            max_threshold_15min += end_signal_15min * signal_15min
            # 降下条件
            decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min

            sell = self.and_gate(
                self.is_exceed(max_threshold_15min, self.max_histogram_15min),
                self.is_exceed(histogram_15min, decrease_threshold_15min),
            )

            if sell:
                operation = self.SELL
            else:
                operation = self.STAY
        else:
            operation = self.STAY

        return operation
