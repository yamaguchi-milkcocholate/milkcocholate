import numpy as np
from modules.fitnessfunction.fitnessfunction import FitnessFunction
from modules.datamanager.zigzag import ZigZag


class ZigZagFunction(FitnessFunction):
    FITNESS_FUNCTION_ID = 7
    DEFAULT_YEN_POSITION = 1000
    COMMISSION = 0.0015

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
        deviation = genome[1]
        coin = 0
        has_coin = False
        loss = 0
        loss_count = 0
        benefit = 0
        benefit_count = 0
        fitness = 0
        max_high = float(self.__data.loc[0].high)
        min_low = float(self.__data.loc[0].low)
        max_high_i = 0
        min_low_i = 0
        last_depth = depth
        top_i = 0
        bottom_i = 0

        buy_fail = 0
        sell_fail = 0
        buy_transaction = 0
        sell_trasaction = 0

        for data_i in range(1, len(self.__data)):
            high = float(self.__data.loc[data_i].high)
            low = float(self.__data.loc[data_i].low)

            if max_high < high:
                max_high = high
                max_high_i = data_i
            if min_low > low:
                min_low = low
                min_low_i = data_i

            top = self.and_gate(
                min_low * (1 + deviation) < max_high,
                min_low_i < max_high_i,
                last_depth + (max_high_i - bottom_i) > depth,
            )
            bottom = self.and_gate(
                max_high * (1 - deviation) > min_low,
                max_high_i < min_low_i,
                last_depth + (min_low_i - top_i) > depth,
            )

            # 右肩上がりの線を引く (売りのエントリー)
            if top:
                top_i = data_i
                min_low = low
                min_low_i = data_i

                buy_transaction += 1

                if has_coin:
                    result = float(coin * max_high * (1 - self.COMMISSION))
                    coin = 0

                    # プラスかマイナスか
                    if result < 0:
                        loss += result
                        loss_count += 1
                    else:
                        benefit += result
                        benefit_count += 1
                    has_coin = False
                else:
                    buy_fail += 1

            # 右肩下がりの線を引く (買いのエントリー)
            if bottom:
                bottom_i = data_i
                max_high = high
                max_high_i = data_i

                sell_trasaction += 1

                if not has_coin:
                    coin = float(self.DEFAULT_YEN_POSITION * (1 - self.COMMISSION) / min_low)
                    has_coin = True
                else:
                    sell_fail += 1

        fitness = benefit + loss
        print(
            'fitness',
            fitness,
            'buy fail',
            buy_fail,
            'sell fail',
            sell_fail,
            'benefit',
            benefit,
            'count',
            benefit_count,
            'loss',
            loss,
            'count',
            loss_count,
            'total',
            fitness,
            'count',
            benefit_count + loss_count,
            'buy transaction',
            buy_transaction,
            'sell transaction',
            sell_trasaction
        )
        return fitness

    @staticmethod
    def and_gate(*args):
        return all(args)

    def calc_result_and_log(self, population_id, **kwargs):
        pass
