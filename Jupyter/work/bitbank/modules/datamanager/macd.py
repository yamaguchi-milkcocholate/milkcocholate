import pandas as pd
import numpy as np
import pickle
import sys
import os
from modules.datamanager.picker import Picker


class MACD:

    def __init__(self, use_of_data='training'):
        picker = Picker(span='5min', use_of_data=use_of_data, coin='xrp', is_inclination=False)
        self.candlestick = picker.get_candlestick()
        self.short_term = None
        self.long_term = None
        self.signal = None
        self.__is_validation = None

    def __call__(self, short_term=12, long_term=26, signal=9, is_pickle=False, is_validation=False):
        """
        :param short_term: float 短期間の平滑移動平均
        :param long_term:  float 長期間の平滑移動平均
        :param signal:     float シグナルの平滑移動平均
        :return:           pandas.DataFrame
        """
        self.short_term = short_term
        self.long_term = long_term
        self.signal = signal
        self.__is_validation = is_validation
        signal = self.calculate(is_pickle=is_pickle)
        return signal

    def calculate(self, is_pickle):
        """
        15min       EMA
        5min        EMA
        1min + 5min EMA
        """
        if is_pickle is False:
            data_15min, data_5min = self.normalize_data()
            macd, data_15min, data_5min = self.first_sma_data_frame(data_15min, data_5min)
            macd = self.macd_data_frame(macd, data_5min)
            signal = self.macd_signal_data_frame(macd)
            self.__write_signal(signal=signal)
        else:
            signal = self.__read_signal()
        return signal

    def macd_signal_data_frame(self, macd):
        """
        MACDシグナル
        :param macd: pandas.DataFrame
        :return:     pandas.DataFrame
        """
        part = macd.loc[:self.signal * 3 - 1]
        sma_15min = float(np.sum(np.unique(part.macd_15min.values)) / self.signal)
        sma_5min = float(np.sum(part.loc[self.signal * 2:].macd_5min.values) / self.signal)
        macd = macd.loc[self.signal * 3:].reset_index(drop=True)
        signal = pd.DataFrame([[
            part.tail(1).price,
            part.tail(1).macd_15min,
            part.tail(1).macd_5min,
            sma_15min,
            sma_5min,
            part.tail(1).macd_15min - sma_15min,
            part.tail(1).macd_5min - sma_5min,
            part.tail(1).time
        ]], columns=[
            'price',
            'macd_15min',
            'macd_5min',
            'signal_15min',
            'signal_5min',
            'histogram_15min',
            'histogram_5min',
            'time'
        ])
        signal_15min = sma_15min
        signal_5min = sma_5min
        print('signal')
        for macd_i in range(len(macd) - 1):
            sys.stdout.write("\r%d" % int(macd_i + 1))
            sys.stdout.flush()
            signal_15min = self.__exponential_moving_average(
                value=macd.loc[macd_i].macd_15min,
                pre_value=signal_15min,
                term=self.signal
            )
            signal_5min = self.__exponential_moving_average(
                value=macd.loc[macd_i].macd_5min,
                pre_value=signal_5min,
                term=self.signal
            )
            signal.loc[macd_i + 1] = [
                macd.loc[macd_i].price,
                macd.loc[macd_i].macd_15min,
                macd.loc[macd_i].macd_5min,
                signal_15min,
                signal_5min,
                macd.loc[macd_i].macd_15min - signal_15min,
                macd.loc[macd_i].macd_5min - signal_5min,
                macd.loc[macd_i].time,
            ]
        print()
        return signal.loc[1:].reset_index(drop=True)

    def macd_data_frame(self, ema, data_5min):
        """
        平滑移動平均
        :param ema:        pandas.DataFrame
        :param data_5min:  pandas.DataFrame
        :return:           pandas.DataFrame
        """
        ema_15min_short = ema.loc[0].short_15min
        ema_15min_long = ema.loc[0].long_15min
        ema_5min_short = ema.loc[0].short_5min
        ema_5min_long = ema.loc[0].long_5min
        print('macd')
        for i_5min in range(len(data_5min) - 1):
            sys.stdout.write("\r%d" % int(i_5min + 1))
            sys.stdout.flush()
            if i_5min % 15 == 0 and i_5min != 0:
                ema_15min_short = self.__exponential_moving_average(
                    value=data_5min.loc[i_5min].end,
                    pre_value=ema_15min_short,
                    term=self.short_term
                )
                ema_15min_long = self.__exponential_moving_average(
                    value=data_5min.loc[i_5min].end,
                    pre_value=ema_15min_long,
                    term=self.long_term
                )
            ema_5min_short = self.__exponential_moving_average(
                value=data_5min.loc[i_5min].end,
                pre_value=ema_5min_short,
                term=self.short_term
            )
            ema_5min_long = self.__exponential_moving_average(
                value=data_5min.loc[i_5min].end,
                pre_value=ema_5min_long,
                term=self.long_term
            )
            ema.loc[i_5min + 1] = [
                data_5min.loc[i_5min + 1].end,
                ema_15min_short,
                ema_15min_long,
                ema_5min_short,
                ema_5min_long,
                ema_15min_short - ema_15min_long,
                ema_5min_short - ema_5min_long,
                data_5min.loc[i_5min].time,
            ]
        print()
        return ema.loc[1:].reset_index(drop=True)

    @staticmethod
    def __exponential_moving_average(value, pre_value, term):
        return pre_value + (2 / (term + 1)) * (value - pre_value)

    def first_sma_data_frame(self, data_15min, data_5min):
        """
        最初は単純移動平均
        :param data_15min: pandas.DataFrame
        :param data_5min: pandas.DataFrame
        :return: pandas.DataFrame, pandas.DataFrame, pandas.DataFrame
        ['short_15min', 'long_15min', 'short_5min', 'long_5min''], candlestick_15min, candlestick_5min
        """
        sma_15min_short = self.sma_15min_short(data_15min)[0]
        sma_15min_long = self.sma_15min_long(data_15min)[0]
        data_15min = self.cut_for_ema_15min(data_15min)
        sma_5min_short = self.sma_5min_short(data_5min)[0]
        sma_5min_long = self.sma_5min_long(data_5min)[0]
        data_5min = self.cut_for_ema_5min(data_5min)
        ema = pd.DataFrame([[
            data_5min.loc[0].end,
            sma_15min_short,
            sma_15min_long,
            sma_5min_short,
            sma_5min_long,
            sma_15min_short - sma_15min_long,
            sma_5min_short - sma_5min_long,
            data_5min.loc[0, 'time']
        ]], columns=[
            'price',
            'short_15min',
            'long_15min',
            'short_5min',
            'long_5min',
            'macd_15min',
            'macd_5min',
            'time'
        ])
        return ema, data_15min, data_5min

    def sma_15min_short(self, data_15min):
        """
        15minの短期単純移動平均
        :param data_15min:
        :return: SMA, テスト用DataFrame
        """
        part = data_15min.loc[(self.long_term - self.short_term):self.long_term - 1]
        price_sum = np.sum(part.end.values)
        sma = float(price_sum / self.short_term)
        return sma, part

    def sma_15min_long(self, data_15min):
        """
        15minの長期単純移動平均
        :param data_15min:
        :return: SMA, テスト用DataFrame
        """
        part = data_15min.loc[0: self.long_term - 1]
        price_sum = np.sum(part.end.values)
        sma = float(price_sum / self.long_term)
        return sma, part

    def sma_5min_short(self, data_5min):
        """
        5minの短期単純移動平均
        :param data_5min:
        :return: SMA, テスト用のDataFrame
        """
        # 15 = 5 * 3
        part = data_5min.loc[self.long_term * 3 - self.short_term:self.long_term * 3 - 1]
        price_sum = np.sum(part.end.values)
        sma = float(price_sum / self.short_term)
        return sma, part

    def sma_5min_long(self, data_5min):
        """
        5minの長期単純移動平均
        :param data_5min:
        :return: SMA, テスト用のDataFrame
        """
        # 15 = 5 * 3
        part = data_5min.loc[self.long_term * 3 - self.long_term:self.long_term * 3 - 1]
        price_sum = np.sum(part.end.values)
        sma = float(price_sum / self.long_term)
        return sma, part

    def normalize_data(self):
        """
        15, 5の倍数に揃える
        :return:
        """
        self.candlestick = self.candlestick.loc[0:len(self.candlestick) - len(self.candlestick) % 15 - 1]
        data_15min = self.candlestick.loc[::3].reset_index(drop=True)
        return data_15min, self.candlestick

    def cut_for_ema_15min(self, data_15min):
        """
        SMAで使った部分を切り捨てる
        :param data_15min:
        :return:
        """
        return data_15min[self.long_term:].reset_index(drop=True)

    def cut_for_ema_5min(self, data_5min):
        """
        SMAで使った部分を切り捨てる
        :param data_5min:
        :return:
        """
        return data_5min[self.long_term * 3:].reset_index(drop=True)

    def __write_signal(self, signal):
        if self.__is_validation:
            our = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../5min/macd/signal_short.pickle')
        else:
            our = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../5min/macd/signal.pickle')
        with open(our, 'wb') as f:
            pickle.dump(signal, f)

    def __read_signal(self):
        if self.__is_validation:
            our = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../5min/macd/signal_short.pickle')
        else:
            our = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + '/../../5min/macd/signal.pickle')
        with open(our, 'rb') as f:
            signal = pickle.load(f)
        return signal
