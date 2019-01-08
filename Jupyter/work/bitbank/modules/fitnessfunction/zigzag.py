import numpy as np
import math
from modules.fitnessfunction.fitnessfunction import FitnessFunction
from modules.datamanager.zigzag import ZigZag


class ZigZagFunction(FitnessFunction):
    FITNESS_FUNCTION_ID = 7
    DEFAULT_YEN_POSITION = 1000
    COMMISSION = 0.0015
    BENEFIT_RATE = 0.01

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
        depth = genome[0]
        buy_deviation = genome[1]
        sell_deviation = genome[2]
        coin = 0
        has_coin = False
        loss = 0
        loss_count = 0
        benefit = 0
        benefit_count = 0
        max_high = float(self.__data.loc[0].high)
        min_low = float(self.__data.loc[0].low)
        max_high_i = 0
        min_low_i = 0
        last_depth = depth
        top_i = 0
        bottom_i = 0

        goal_match = 0

        for data_i in range(1, len(self.__data)):
            high = float(self.__data.loc[data_i].high)
            low = float(self.__data.loc[data_i].low)
            price = float(self.__data.loc[data_i].end)

            if max_high < high:
                max_high = high
                max_high_i = data_i
            if min_low > low:
                min_low = low
                min_low_i = data_i

            top = self.and_gate(
                min_low * (1 + sell_deviation) < max_high,
                min_low_i < max_high_i,
                last_depth + (max_high_i - bottom_i) > depth,
            )
            bottom = self.and_gate(
                max_high * (1 - buy_deviation) > min_low,
                max_high_i < min_low_i,
                last_depth + (min_low_i - top_i) > depth,
            )

            # 右肩上がりの線を引く (売りのエントリー)
            if top:
                last_depth = data_i - bottom_i
                top_i = data_i
                min_low = low
                min_low_i = data_i

                if has_coin:
                    result = float(coin * price * (1 - self.COMMISSION)) - self.DEFAULT_YEN_POSITION
                    coin = 0

                    # プラスかマイナスか
                    if result < 0:
                        loss += result
                        loss_count += 1
                    else:
                        benefit += result
                        benefit_count += 1
                        if result > self.DEFAULT_YEN_POSITION * self.BENEFIT_RATE:
                            goal_match += 1
                        else:
                            pass
                    has_coin = False

            # 右肩下がりの線を引く (買いのエントリー)
            elif bottom:
                last_depth = data_i - top_i
                bottom_i = data_i
                max_high = high
                max_high_i = data_i

                if not has_coin:
                    coin = float(self.DEFAULT_YEN_POSITION * (1 - self.COMMISSION) / price)
                    has_coin = True

        tmp = benefit + loss
        fitness = self.__fitness(benefit=benefit, loss=loss, transaction=benefit_count + loss_count, goal_match=goal_match)
        print(
            'fitness',
            fitness,
            'total',
            tmp,
            'count',
            goal_match,
            '/',
            benefit_count + loss_count,
            'benefit',
            benefit,
            'count',
            benefit_count,
            'loss',
            loss,
            'count',
            loss_count,
            'depth',
            depth,
            'buy deviation',
            buy_deviation,
            'sell deviation',
            sell_deviation
        )
        return fitness

    @staticmethod
    def __fitness(benefit, loss, goal_match, transaction):
        if benefit + loss < 0:
            return 0
        else:
            fitness = 100 * (benefit / -loss) + 50 * (goal_match / transaction)
            fitness *= math.log((benefit + loss + 1), 10)
        return fitness

    @staticmethod
    def and_gate(*args):
        return all(args)

    def calc_result_and_log(self, population_id, **kwargs):
        pass
