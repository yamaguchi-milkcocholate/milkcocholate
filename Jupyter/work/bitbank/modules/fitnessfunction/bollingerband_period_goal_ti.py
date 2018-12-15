from modules.datamanager import bollingerband
from modules.fitnessfunction.fitnessfunction import FitnessFunction
from modules.datamanager import functions
from enum import IntEnum
import numpy as np
import math


class BollingerBandPeriodGoalTi(FitnessFunction):
    FITNESS_FUNCTION_ID = 4

    UPPER = 0
    UPPER_UPPER = 1
    UPPER_MIDDLE = 2
    MIDDLE_LOWER = 3
    LOWER_LOWER = 4
    LOWER = 5

    POSITIVE_INCLINATION = 1.376
    NEGATIVE_INCLINATION = -1.376
    POSITIVE_MIDDLE_INCLINATION = 0.325
    NEGATIVE_MIDDLE_INCLINATION = -0.325

    HYPER_EXPANSION = 0
    EXPANSION = 1
    FLAT = 2
    SQUEEZE = 3
    HYPER_SQUEEZE = 4

    GOAL_RATE = 1.1
    FITNESS_PRODUCTION = 10
    LOSS_CUT_RATE = 0.95
    """
    1. 標準偏差σを線形回帰(次数M)
    2. 前回と現在のボラティリティーと終値の位置
    """

    def __init__(self, candle_type, db_dept, hyper_paras, coin):
        """
        :param candle_type:
        :param db_dept:
        :param hyper_paras:
        """
        super().__init__(
            candle_type=candle_type,
            db_dept=db_dept,
            fitness_function_id=self.FITNESS_FUNCTION_ID,
            coin=coin
        )
        self._approach = bollingerband.BollingerBand(candlestick=self._candlestick)
        self._data = self._approach(
            sma_term=hyper_paras['sma_term'],
            std_term=hyper_paras['std_term']
        )
        self._last_data_num = hyper_paras['last_data_num']
        self._inclination_alpha = hyper_paras['inclination_alpha']
        self.__loss_cut = 0

    def calc_fitness(self, geno_type, should_log, population_id):
        """
        適応度を計算
        :param geno_type:       numpy   遺伝子
        :param should_log:      bool    記録を取るかどうか
        :param population_id:   int     テーブル'populations'のid
        :return:                numpy   適応度
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
            genome = geno_type[genome_i]
            fitness_result = self.calc_result(genome=genome)
            fitness_list.append(fitness_result)
        return np.asarray(a=fitness_list, dtype=np.int32)

    def calc_result(self, **kwargs):
        """
        過去のデータから取引を行って、10%の利益率で区切りをつける
        :return:     int              利益率10%をどのくらい達成できたか * FITNESS_PRODUCTION * 成立した取引率
        """
        genome = kwargs['genome']
        # ポジションを初期化
        bitcoin, yen, has_bitcoin = self.init_position()
        # 目標値を設定
        goal_bitcoin, goal_yen = self.init_goal(data_i=0)
        fitness = 0
        last_end_position = self.end_position(data_i=self._last_data_num - 2)
        for data_i in range(self._last_data_num - 1, len(self._data)):
            inclination_pattern = self.inclination(data_i=data_i)
            end_position = self.end_position(data_i=data_i)
            operation = BollingerBandOperationTi.operation(
                last_end_position=last_end_position,
                end_position=end_position,
                inclination_pattern=inclination_pattern,
                genome=genome,
                has_bitcoin=has_bitcoin
            )
            last_end_position = end_position
            if int(operation) is int(BollingerBandOperationTi.BUY):
                if has_bitcoin is False:
                    has_bitcoin = True
                    end_price = self._data.loc[data_i, 'end']
                    bitcoin = float(yen / end_price)
                    yen = 0
                    # 目標達成!
                    if bitcoin > goal_bitcoin:
                        # 適応度を更新
                        fitness = self.goal(fitness=fitness)
                        # 目標を更新
                        goal_bitcoin, goal_yen = self.init_goal(data_i=data_i)
                        # ポジションを初期化
                        bitcoin, yen, has_bitcoin = self.init_position()
                    # 損切
                    elif bitcoin < self.INIT_BIT_COIN_AMOUNT * self.LOSS_CUT_RATE:
                        # 目標を更新
                        goal_bitcoin, goal_yen = self.init_goal(data_i=data_i)
                        # ポジションを初期化
                        bitcoin, yen, has_bitcoin = self.init_position()
                        self.__loss_cut += 1
                else:
                    # 取引失敗
                    pass
            elif int(operation) is int(BollingerBandOperationTi.SELL):
                if has_bitcoin is True:
                    has_bitcoin = False
                    end_price = self._data.loc[data_i, 'end']
                    yen = float(bitcoin * end_price)
                    bitcoin = 0
                    # 目標達成!
                    if yen > goal_yen:
                        # 適応度を更新
                        fitness = self.goal(fitness=fitness)
                        # 目標を更新
                        goal_bitcoin, goal_yen = self.init_goal(data_i=data_i)
                        # ポジションを初期化
                        bitcoin, yen, has_bitcoin = self.init_position()
                    # 損切
                    elif yen < self.INIT_BIT_COIN_AMOUNT * end_price * self.LOSS_CUT_RATE:
                        # 目標を更新
                        goal_bitcoin, goal_yen = self.init_goal(data_i=data_i)
                        # ポジションを初期化
                        bitcoin, yen, has_bitcoin = self.init_position()
                        self.__loss_cut += 1
                else:
                    # 取引失敗
                    pass
        # 適応度を更新
        goal = fitness
        fitness = self.loss_cut(fitness=fitness)
        # 目標達成の度合いを返す(適応度)
        print('finally',
              'goal',
              goal,
              'fitness',
              fitness,
              'loss cut',
              str(self.__loss_cut)
              )
        self.__loss_cut = 0
        return fitness

    def calc_result_and_log(self, population_id, **kwargs):
        """
        過去のデータから取引を行って、10%の利益率で区切りをつける
        記録をデータベースに保存する
        :param population_id:   int              テーブル'populations'のid
        :return:                int              利益率10%をどのくらい達成できたか * FITNESS_PRODUCTION * 成立した取引率
        """
        insert_list = list()
        str_format = '%Y-%m-%d %H:%M:%S'
        genome = kwargs['genome']
        # ポジションを初期化
        bitcoin, yen, has_bitcoin = self.init_position()
        # 目標値を設定
        goal_bitcoin, goal_yen = self.init_goal(data_i=0)
        # 確定利益
        profit = 0
        fitness = 0
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
            operation = BollingerBandOperationTi.operation(
                last_end_position=last_end_position,
                end_position=end_position,
                inclination_pattern=inclination_pattern,
                genome=genome,
                has_bitcoin=has_bitcoin
            )
            last_end_position = end_position
            if int(operation) is int(BollingerBandOperationTi.BUY):
                if has_bitcoin is False:
                    has_bitcoin = True
                    end_price = self._data.loc[data_i, 'end']
                    bitcoin = float(yen / end_price)
                    yen = 0
                    # DB
                    time = self._data.loc[data_i, 'time'].strftime(str_format)
                    insert_list.append([
                        population_id,
                        int(bitcoin * end_price + profit),
                        int(end_price),
                        time
                    ])
                    # 目標達成!
                    if bitcoin > goal_bitcoin:
                        # 適応度を更新
                        fitness = self.goal(fitness=fitness)
                        # 目標を更新
                        goal_bitcoin, goal_yen = self.init_goal(data_i=data_i)
                        # 確定利益を更新
                        profit += (bitcoin * end_price - end_price)
                        # ポジションを初期化
                        bitcoin, yen, has_bitcoin = self.init_position()
                        time = self._data.loc[data_i, 'time'].strftime(str_format)
                        # 同じ時間で初期化後のデータを入力
                        # 確定利益 + 1bitcoin(=終値)
                        insert_list.append([
                            population_id,
                            int(end_price + profit),
                            int(end_price),
                            time
                        ])
                    # 損切
                    elif bitcoin < self.INIT_BIT_COIN_AMOUNT * self.LOSS_CUT_RATE:
                        # 目標を更新
                        goal_bitcoin, goal_yen = self.init_goal(data_i=data_i)
                        # ポジションを初期化
                        bitcoin, yen, has_bitcoin = self.init_position()
                        self.__loss_cut += 1
                else:
                    # 取引失敗
                    pass
            elif int(operation) is int(BollingerBandOperationTi.SELL) and has_bitcoin is True:
                if has_bitcoin is True:
                    has_bitcoin = False
                    end_price = self._data.loc[data_i, 'end']
                    yen = float(bitcoin * end_price)
                    bitcoin = 0
                    # DB
                    time = self._data.loc[data_i, 'time'].strftime(str_format)
                    insert_list.append([
                        population_id,
                        int(yen + profit),
                        int(end_price),
                        time
                    ])
                    # 目標達成!
                    if yen > goal_yen:
                        # 適応度を更新
                        fitness = self.goal(fitness=fitness)
                        # 目標を更新
                        goal_bitcoin, goal_yen = self.init_goal(data_i=data_i)
                        # 確定利益を更新
                        profit += (yen - end_price)
                        # ポジションを初期化
                        bitcoin, yen, has_bitcoin = self.init_position()
                        # 同じ時間で初期化後のデータを入力
                        # 確定利益 + 1bitcoin(=終値)
                        insert_list.append([
                            population_id,
                            int(end_price + profit),
                            int(end_price),
                            time
                        ])
                    # 損切
                    elif yen < self.INIT_BIT_COIN_AMOUNT * end_price * self.LOSS_CUT_RATE:
                        # 目標を更新
                        goal_bitcoin, goal_yen = self.init_goal(data_i=data_i)
                        # ポジションを初期化
                        bitcoin, yen, has_bitcoin = self.init_position()
                        self.__loss_cut += 1
                else:
                    # 取引失敗
                    pass
            if len(insert_list) >= 1:
                self._db_dept.give_writer_task(insert_list)
                insert_list = []
        # 一行ずつ挿入 Todo:writerのバグを直す
        if len(insert_list) > 0:
            self._db_dept.give_writer_task(insert_list)
        del insert_list
        # 適応度を更新
        goal = fitness
        fitness = self.loss_cut(fitness=fitness)
        # 目標達成の度合いを返す(適応度)
        print('finally',
              'goal',
              goal,
              'fitness',
              fitness,
              'loss cut',
              str(self.__loss_cut)
              )
        self.__loss_cut = 0
        return fitness

    def inclination(self, data_i):
        """
        標準偏差の傾きを調べる。ボラティリティの広がりをパターンに分ける
        :param data_i: int
        :return: int: 定数、傾きのパターン
        """
        pre_data = self._data.loc[data_i - self._last_data_num + 1:data_i, 'sigma'].values
        min_price = np.amin(pre_data)
        t = pre_data - np.full_like(a=pre_data, fill_value=min_price)
        t = t * 1000
        x = np.arange(
            start=0,
            step=self._inclination_alpha,
            stop=self._inclination_alpha * len(t)
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
        """
        ボラティリティと終値の位置を調べる
        :param data_i: int
        :return: int 位置のパターン
        """
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

    @staticmethod
    def goal(fitness):
        """
        適応度を更新
        :param fitness: int 適応度
        :return:        int 更新した適応度
        """
        return fitness + 1

    def loss_cut(self, fitness):
        """
        fitness = G - 1/2 * G * (log2(L + 1))^2
        :param fitness: integer 適応度
        :return: 損切を含めた適応度
        """
        fitness = fitness - 0.5 * fitness * (math.log(self.__loss_cut, 2))
        if fitness <= 0:
            fitness = 1
        return fitness

    def init_position(self):
        """
        ポシションを初期化する
        :return: int, int, bool:  ビットコインの初期値, 円の初期値, ビットコインを持っているかどうか
        """
        return self.INIT_BIT_COIN_AMOUNT, 0, True

    def init_goal(self, data_i):
        """
        目標値を初期化する
        :param data_i:  int     いつの取得データか特定する
        :return: float, float   ビットコインの目標値, 円の目標値
        """
        return self.INIT_BIT_COIN_AMOUNT * self.GOAL_RATE, self._data.at[data_i, 'end'] * self.GOAL_RATE


class BollingerBandOperationTi(IntEnum):
    """
    bitcoinの 買い、売り、保持を示すEnum
    """
    BUY = 1
    STAY = 2
    SELL = 3

    @staticmethod
    def operation(last_end_position, end_position, inclination_pattern, genome, has_bitcoin):
        """
        終値、上部バンド、下部バンドから(買い,売り,保持)を決める
        ※ 遺伝子の特徴
        [(前回の終値位置0~5 * 1)(現在の終値位置0~5 * 6)(傾きのパターン0~4 * 36)(ビットコインを持っているか0~1 * 180)]
        """
        if has_bitcoin:
            has_bitcoin = 1
        else:
            has_bitcoin = 0
        return genome[last_end_position * 1 + end_position * 6 + inclination_pattern * 36 + has_bitcoin * 180]
