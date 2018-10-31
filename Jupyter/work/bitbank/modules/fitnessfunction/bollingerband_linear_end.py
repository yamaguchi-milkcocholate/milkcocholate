from modules.datamanager import bollingerband
from modules.fitnessfunction import fitnessfunction
from modules.datamanager import functions
import numpy as np
from enum import Enum


class BollingerBandLinearEnd(fitnessfunction.FitnessFunction):
    UPPER = 0
    UPPER_UPPER = 1
    UPPER_MIDDLE = 2
    MIDDLE_LOWER = 3
    LOWER_LOWER = 4
    LOWER = 5

    POSITIVE_INCLINATION = 1
    NEGATIVE_INCLINATION = -1
    POSITIVE_MIDDLE_INCLINATION = 1.7
    NEGATIVE_MIDDLE_INCLINATION = -1.7

    HYPER_EXPANSION = 0
    EXPANSION = 1
    FLAT = 2
    SQUEEZE = 3
    HYPER_SQUEEZE = 4

    """
    1. 標準偏差σを線形回帰(次数M)
    2. 直近の終値とボリンジャーバンドの位置
    """

    def __init__(self, candle_type, db_dept, fitness_function_id, hyper_params):
        """

        :param candle_type:
        :param db_dept:
        :param fitness_function_id:
        :param hyper_params:
        ['sma_term', 'std_term', 'linear_dim', 'last_data_num']
        """
        super().__init__(
            candle_type=candle_type,
            db_dept=db_dept,
            fitness_function_id=fitness_function_id
        )
        self._approach = bollingerband.BollingerBand(candlestick=self._candlestick)
        # 平均移動戦と標準偏差はハイパーパラメータなので最初に計算するだけ
        self._data = self._approach(
            sma_term=hyper_params['sma_term'],
            std_term=hyper_params['std_term']
        )
        self._last_data_num = hyper_params['last_data_num']
        self._inclination_alpha = hyper_params['inclination_alpha']

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
        if should_log:
            # FitnessFunctionの抽象クラス制約で冗長な引数
            fitness_result = self.calc_result_and_log(
                population_id=population_id,
                genome=genome
            )
        else:
            # FitnessFunctionの抽象クラス制約で冗長な引数
            fitness_result = self.calc_result(genome=genome)
        fitness_list.append(fitness_result)
        # 2番目以降の個体
        for genome_i in range(1, population):
            genome = geno_type(genome_i)
            fitness_result = self.calc_result(genome=genome)
            fitness_list.append(fitness_result)
        return np.asarray(a=fitness_list, dtype=np.int32)

    def calc_result(self, **kwargs):
        """
        過去のデータから取引を行って、最終日の持ち分を適応度とする
        :return:     int              最終日の持ち分(円)
        """
        genome = kwargs['genome']
        bitcoin = self.INIT_BIT_COIN_AMOUNT
        yen = 0
        has_bitcoin = True
        last_end_position = self.end_position(data_i=self._last_data_num - 2)
        for data_i in range(self._last_data_num - 1, len(self._data)):
            inclination_pattern = self.inclination(data_i=data_i)
            end_position = self.end_position(data_i=data_i)
            operation = BollingerBandLinearEndOperation.operation(
                last_end_position=last_end_position,
                end_position=end_position,
                inclination_pattern=inclination_pattern,
                genome=genome
            )
            last_end_position = end_position
            if operation is BollingerBandLinearEndOperation.BUY and has_bitcoin is False:
                has_bitcoin = True
                end_price = self._data.loc[data_i, 'end']
                bitcoin = float(yen / end_price)
                yen = 0
                print(self._data.loc[data_i, 'time'], end_price, 'buy', 'bitcoin', bitcoin)
            elif operation is BollingerBandLinearEndOperation.SELL and has_bitcoin is True:
                has_bitcoin = False
                end_price = self._data.loc[data_i, 'end']
                yen = float(bitcoin * end_price)
                bitcoin = 0
                print(self._data.loc[data_i, 'time'], end_price, 'sell', 'yen', yen)
        if has_bitcoin is True:
            yen = float(bitcoin * self._data.tail(1)['end'])
        print('finally', 'yen', yen)
        return int(yen)

    def calc_result_and_log(self, population_id, **kwargs):
        """
        過去のデータから取引を行って、最終日の持ち分を適応度とする
        記録をデータベースに保存する
        :param population_id:   int              テーブル'populations'のid
        :return:                int              最終日の持ち分(円)
        """
        insert_list = list()
        str_format = '%Y-%m-%d %H:%M:%S'
        genome = kwargs['genome']
        bitcoin = self.INIT_BIT_COIN_AMOUNT
        yen = 0
        has_bitcoin = True
        # 0番目の結果
        insert_list.append([
            population_id,
            int(bitcoin * self._data.at[0, 'end']),
            int(bitcoin * self._data.at[0, 'end']),
            self._data.at[0, 'time'].strftime(str_format)
        ])
        last_end_position = self.end_position(data_i=self._last_data_num - 2)
        for data_i in range(self._last_data_num - 1, len(self._data)):
            inclination_pattern = self.inclination(data_i=data_i)
            end_position = self.end_position(data_i=data_i)
            operation = BollingerBandLinearEndOperation.operation(
                last_end_position=last_end_position,
                end_position=end_position,
                inclination_pattern=inclination_pattern,
                genome=genome
            )
            last_end_position = end_position
            if operation is BollingerBandLinearEndOperation.BUY and has_bitcoin is False:
                has_bitcoin = True
                end_price = self._data.loc[data_i, 'end']
                time = self._data.loc[data_i, 'time'].strgtime(str_format)
                bitcoin = float(yen / end_price)
                yen = 0
                print(time, end_price, 'buy', 'bitcoin', bitcoin)
                # DB
                insert_list.append([
                    population_id,
                    int(bitcoin * end_price),
                    int(end_price),
                    time
                ])
            elif operation is BollingerBandLinearEndOperation.SELL and has_bitcoin is True:
                has_bitcoin = False
                end_price = self._data.loc[data_i, 'end']
                time = self._data.loc[data_i, 'time'].strgtime(str_format)
                yen = float(bitcoin * end_price)
                bitcoin = 0
                print(time, end_price, 'sell', 'yen', yen)
                # DB
                insert_list.append([
                    population_id,
                    int(yen),
                    int(end_price),
                    time
                ])
            if len(insert_list) >= self.BATCH_INSERT_NUM:
                self._db_dept.give_writer_task(insert_list)
                insert_list = []
        if has_bitcoin is True:
            yen = float(bitcoin * self._data.tail(1)['end'])
        print('finally', 'yen', yen)
        if len(insert_list) > 0:
            self._db_dept.give_writer_task(insert_list)
        del insert_list
        return int(yen)

    def inclination(self, data_i):
        pre_data = self._data.loc[data_i - self._last_data_num + 1:data_i, 'sigma'].values
        min_price = np.amin(pre_data)
        t = pre_data - np.full_like(a=pre_data, fill_value=min_price)
        x = np.arange(
            start=0,
            step=self._inclination_alpha,
            stop=self._inclination_alpha * (len(t) - 1)
        )
        inclination = functions.linear_regression(
            x=x,
            t=t,
            basic_function=functions.Polynomial(dim=2)
        )[1]

        if self.POSITIVE_INCLINATION < inclination:
            inclination_pattern = self.HYPER_EXPANSION
        elif (self.POSITIVE_MIDDLE_INCLINATION < inclination) and (inclination <= self.POSITIVE_INCLINATION):
            inclination_pattern = self.EXPANSION
        elif (self.NEGATIVE_MIDDLE_INCLINATION <= inclination) and (inclination <= self.POSITIVE_MIDDLE_INCLINATION):
            inclination_pattern = self.FLAT
        elif (self.NEGATIVE_INCLINATION <= inclination) and (inclination < self.NEGATIVE_MIDDLE_INCLINATION):
            inclination_pattern = self.SQUEEZE
        elif inclination < self.NEGATIVE_INCLINATION:
            inclination_pattern = self.HYPER_SQUEEZE
        else:
            inclination_pattern = None
        return inclination_pattern

    def end_position(self, data_i):
        end_price = self._data.loc[data_i, 'end']
        lower_band = self._data.loc[data_i, 'lower_band']
        lower_band_double = self._data.loc[data_i, 'lower_band_double']
        upper_band = self._data.loc[data_i, 'upper_band']
        upper_band_double = self._data.loc[data_i, 'upper_band_double']
        sma = self._data.loc[data_i, 'simple_moving_average']
        if upper_band_double < end_price:
            return self.UPPER
        elif (upper_band < end_price) and (end_price <= upper_band_double):
            return self.UPPER_UPPER
        elif (sma < end_price) and (end_price <= upper_band):
            return self.UPPER_MIDDLE
        elif (lower_band <= end_price) and (end_price <= sma):
            return self.MIDDLE_LOWER
        elif (lower_band_double <= end_price) and (end_price < lower_band):
            return self.LOWER_LOWER
        elif end_price < lower_band_double:
            return self.LOWER


class BollingerBandLinearEndOperation(Enum):
    """
    bitcoinの 買い、売り、保持を示すEnum
    """
    BUY = 1
    SELL = 2
    STAY = 3

    @staticmethod
    def operation(last_end_position, end_position, inclination_pattern, genome):
        """
        終値、上部バンド、下部バンドから(買い,売り,保持)を決める
        ※ 遺伝子の特徴
        [(前回の終値位置0~5 * 1)(現在の終値位置0~5 * 6)(傾きのパターン0~n * 36)]
        """
        return genome[last_end_position * 1 + end_position * 6 + inclination_pattern * 36]
