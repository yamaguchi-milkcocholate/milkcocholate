from modules.datamanager import macd
from modules.datamanager import picker
import numpy as np
from enum import Enum


class SimpleMacDParams:
    """
    MACDのパラメータの最適化を行う
    ゴールデンクロスとデッドクロスになったときに全額を取引する単純な方法
    """
    BIT_BANK_CANDLE_STICK = ['5min', '15min', '1hour']

    def __init__(self, candle_type):
        if candle_type in SimpleMacDParams.BIT_BANK_CANDLE_STICK:
            self.picker = picker.Picker(candle_type)
            self.candlestick = self.picker.get_candlestick()
            self.approach = macd.MacD(self.candlestick)
        else:
            raise TypeError('candle type is not found')

    def calc_fitness(self, geno_type):
        """
        calc_resultメソッドより適応度を計算
        :param geno_type: 遺伝子
        :return: numpy    適応度
        """
        population = geno_type.shape[0]
        fitness_list = list()
        for geno_i in range(population):
            geno = geno_type[geno_i]
            data = self.approach(geno[0], geno[1], geno[2])
            fitness_result = self.calc_result(data)
            fitness_list.append(fitness_result)
        return np.asarray(fitness_list, int)

    @staticmethod
    def calc_result(data):
        """
        過去のデータから取引を行って、最終日の持ち分を適応度とする
        :param data: pandas.DataFrame 過去のデータ
        :return:     int              最終日の持ち分(円)
        """
        pre_macd = 0
        pre_signal = 0
        bitcoin = 10
        yen = 0
        has_bitcoin = True
        for row in data.itertuples():
            operation = MacdOperation.operation(pre_macd, pre_signal, row.macd, row.macd_signal, has_bitcoin)
            if operation is MacdOperation.BUY:
                has_bitcoin = False
                yen = float(bitcoin * float(row.end))
                bitcoin = 0
                print(row.time, row.end, 'buy', 'yen', yen)
            elif operation is MacdOperation.SELL:
                has_bitcoin = True
                bitcoin = float(yen / float(row.end))
                yen = 0
                print(row.time, row.end, 'sell', 'bitcoin', bitcoin)
            pre_macd = row.macd
            pre_signal = row.macd_signal
        if has_bitcoin:
            yen = float(bitcoin * float(data.tail(1)['end']))
        print(yen)
        return int(yen)


class MacdOperation(Enum):
    """
    買い、売り、保持を示すEnum
    """
    BUY = 1
    SELL = 2
    STAY = 3

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
        if pre_macd < pre_signal and macd > signal:
            if pre_macd < 0 and pre_signal < 0 and macd < 0 and signal < 0 and has_bitcoin:
                return MacdOperation.BUY
            elif pre_macd > 0 and pre_signal > 0 and macd > 0 and signal > 0 and not has_bitcoin:
                return MacdOperation.SELL
        elif pre_macd > pre_signal and macd < signal:
            if pre_macd < 0 and pre_signal < 0 and macd < 0 and signal < 0 and has_bitcoin:
                return MacdOperation.BUY
            elif pre_macd > 0 and pre_signal > 0 and macd > 0 and signal > 0 and not has_bitcoin:
                return MacdOperation.SELL
        else:
            return MacdOperation.STAY
