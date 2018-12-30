from modules.datamanager import macd
from modules.fitnessfunction import fitnessfunction
import numpy as np
from enum import Enum


class SimpleMacDParams(fitnessfunction.FitnessFunction):
    FITNESS_FUNCTION_ID = 1
    """
    MACDのパラメータの最適化を行う
    ゴールデンクロスとデッドクロスになったときに全額を取引する単純な方法
    """

    def __init__(self, candle_type, db_dept, pair):
        """
        :param candle_type:
        :param db_dept:
        """
        super().__init__(
            candle_type=candle_type,
            db_dept=db_dept,
            fitness_function_id=self.FITNESS_FUNCTION_ID,
            pair=pair
        )
        self._approach = macd.MACD(self._candlestick)

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
        data = self._approach(short_term=genome[0], long_term=genome[1], signal=genome[2])
        if should_log:
            fitness_result = self.calc_result_and_log(
                population_id=population_id,
                data=data
            )
        else:
            fitness_result = self.calc_result(data)
        fitness_list.append(fitness_result)
        # 2番目以降の個体
        for genome_i in range(1, population):
            genome = geno_type[genome_i]
            data = self._approach(short_term=genome[0], long_term=genome[1], signal=genome[2])
            fitness_result = self.calc_result(data=data)
            fitness_list.append(fitness_result)
        del data
        return np.asarray(a=fitness_list, dtype=np.int32)

    def calc_result(self, data):
        """
        過去のデータから取引を行って、最終日の持ち分を適応度とする
        :param data: pandas.DataFrame 過去のデータ
        :return:     int              最終日の持ち分(円)
        """
        pre_macd = 0
        pre_signal = 0
        bitcoin = self.INIT_BIT_COIN_AMOUNT
        yen = 0
        has_bitcoin = True
        for row in data.itertuples():
            operation = MacdOperation.operation(
                pre_macd=pre_macd,
                pre_signal=pre_signal,
                macd=row.macd,
                signal=row.macd_signal,
                has_bitcoin=has_bitcoin
            )
            if operation is MacdOperation.BUY:
                has_bitcoin = True
                bitcoin = float(yen / float(row.end))
                yen = 0
            elif operation is MacdOperation.SELL:
                has_bitcoin = False
                yen = float(bitcoin * float(row.end))
                bitcoin = 0
            pre_macd = row.macd
            pre_signal = row.macd_signal
        if has_bitcoin:
            yen = float(bitcoin * float(data.tail(1)['end']))
        print(yen)
        return int(yen)

    def calc_result_and_log(self, population_id, **kwargs):
        """
        過去のデータから取引を行って、最終日の持ち分を適応度とする
        記録をデータベースに保存する
        :param kwargs:          pandas.DataFrame ['data']過去のデータ
        :param population_id:   int              テーブル'populations'のid
        :return:                int              最終日の持ち分(円)
        """
        data = kwargs['data']
        insert_list = []
        str_format = '%Y-%m-%d %H:%M:%S'
        pre_macd = 0
        pre_signal = 0
        bitcoin = self.INIT_BIT_COIN_AMOUNT
        yen = 0
        has_bitcoin = True
        insert_list.append([
                population_id,
                int(bitcoin * float(data.at[0, 'end'])),
                int(bitcoin * float(data.at[0, 'end'])),
                data.at[0, 'time'].strftime(str_format),
        ])
        insert_iteration = 0
        for row in data.itertuples():
            operation = MacdOperation.operation(
                pre_macd=pre_macd,
                pre_signal=pre_signal,
                macd=row.macd,
                signal=row.macd_signal,
                has_bitcoin=has_bitcoin
            )
            if operation is MacdOperation.BUY:
                has_bitcoin = True
                bitcoin = float(yen / float(row.end))
                yen = 0
                # DB
                insert_list.append([
                    population_id,
                    int(bitcoin * float(row.end)),
                    int(row.end),
                    row.time.strftime(str_format),
                ])
            elif operation is MacdOperation.SELL:
                has_bitcoin = False
                yen = float(bitcoin * float(row.end))
                bitcoin = 0
                # DB
                insert_list.append([
                    population_id,
                    int(yen),
                    int(row.end),
                    row.time.strftime(str_format),
                ])
            pre_macd = row.macd
            pre_signal = row.macd_signal
            # 20
            if insert_iteration % self.BATCH_INSERT_NUM is 0 and len(insert_list) > 0:
                self._db_dept.give_writer_task(insert_list)
                insert_list = []
        if has_bitcoin:
            yen = float(bitcoin * float(data.tail(1)['end']))
        print(yen)
        if len(insert_list) > 0:
            self._db_dept.give_writer_task(insert_list)
        del insert_list
        return int(yen)


class MacdOperation(Enum):
    """
    (bitcoinを)買い、売り、保持を示すEnum
    """
    BUY = 1
    STAY = 2
    SELL = 3

    @staticmethod
    def operation(pre_macd, pre_signal, macd, signal, has_bitcoin):
        """
        MACD,MACDシグナルから(買い、売り、保持)を決める
        :param pre_macd:      float  前回のMACD
        :param pre_signal:    float  前回のMACDシグナル
        :param macd:          float  現在のMACD
        :param signal:        float  現在のMACDシグナル
        :param has_bitcoin:   bool   bitcoinを持っているか(円を持っていないのか)どうか
        :return:              Enum   (買い、売り、保持)
        """
        # MACDがシグナルを上向きに抜くとき
        if pre_macd < pre_signal and macd > signal:
            if pre_macd < 0 and pre_signal < 0 and macd < 0 and signal < 0 and not has_bitcoin:
                return MacdOperation.BUY
            else:
                return MacdOperation.STAY
        # MACDがシグナルを下向きに抜くとき
        elif pre_macd > pre_signal and macd < signal:
            if pre_macd > 0 and pre_signal > 0 and macd > 0 and signal > 0 and has_bitcoin:
                return MacdOperation.SELL
            else:
                return MacdOperation.STAY
        else:
            return MacdOperation.STAY

    def get_fitness_function_id(self):
        return super().get_fitness_function_id()
