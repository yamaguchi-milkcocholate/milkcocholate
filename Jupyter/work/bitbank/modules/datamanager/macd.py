import pandas as pd
import numpy as np
from modules.datamanager.picker import Picker


class MACD:

    def __init__(self):
        picker = Picker(span='5min', use_of_data='training', coin='xrp')
        self.candlestick = picker.get_candlestick()
        self.short_term = None
        self.long_term = None
        self.signal = None

    def __call__(self, short_term=12, long_term=26, signal=9):
        """
        :param short_term: float 短期間の平滑移動平均
        :param long_term:  float 長期間の平滑移動平均
        :param signal:     float シグナルの平滑移動平均
        :return:           pandas.DataFrame
        """
        self.short_term = short_term
        self.long_term = long_term
        self.signal = signal
        return self.calculate()

    def calculate(self):
        """
        15min       EMA
        5min        EMA
        1min + 5min EMA
        """
        data_15min, data_5min, data_1min = self.normalize_data()
        data_1min = self.cut_for_ema_1min(data_1min)
        macd, data_15min, data_5min = self.first_sma_data_frame(data_15min, data_5min)
        macd = self.macd_data_frame(macd, data_15min, data_5min, data_1min)
        signal = self.macd_signal_data_frame(macd)
        return signal

    def macd_signal_data_frame(self, macd):
        """
        MACDシグナル
        :param macd: pandas.DataFrame
        :return:     pandas.DataFrame
        """
        part = macd.loc[:self.signal - 1]
        sma_15min = float(np.sum(part.macd_15min.values) / self.signal)
        sma_5min = float(np.sum(part.macd_5min.values) / self.signal)
        sma_1min = float(np.sum(part.macd_1min.values) / self.signal)
        macd = macd.loc[self.signal:].reset_index(drop=True)
        signal = pd.DataFrame([[
            part.tail(1).price,
            part.tail(1).macd_15min - sma_15min,
            part.tail(1).macd_5min - sma_5min,
            part.tail(1).macd_1min - sma_1min,
            part.tail(1).time
        ]], columns=[
            'price',
            'histogram_15min',
            'histogram_5min',
            'histogram_1min',
            'time'
        ])
        signal_15min = sma_15min
        signal_5min = sma_5min
        signal_1min = sma_1min
        for macd_i in range(len(macd)):
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
            signal_1min = self.__exponential_moving_average(
                value=macd.loc[macd_i].macd_1min,
                pre_value=signal_1min,
                term=self.signal
            )
            signal.loc[macd_i + 1] = [
                macd.loc[macd_i].price,
                macd.loc[macd_i].macd_15min - signal_15min,
                macd.loc[macd_i].macd_5min - signal_5min,
                macd.loc[macd_i].macd_1min - signal_1min,
                macd.loc[macd_i].time,
            ]
        return signal

    def macd_data_frame(self, ema, data_15min, data_5min, data_1min):
        """
        平滑移動平均
        :param ema:        pandas.DataFrame
        :param data_15min: pandas.DataFrame
        :param data_5min:  pandas.DataFrame
        :param data_1min:  pandas.DataFrame
        :return:           pandas.DataFrame
        """
        ema_15min_short = ema.loc[0].short_15min
        ema_15min_long = ema.loc[0].long_15min
        ema_5min_short = ema.loc[0].short_5min
        ema_5min_long = ema.loc[0].long_5min
        i_15min = 1
        i_5min = 1
        for i_1min in range(len(data_1min) - 1):
            if i_1min % 15 == 0 and i_1min != 0:
                ema_15min_short = self.__exponential_moving_average(
                    value=data_15min.loc[i_15min].end,
                    pre_value=ema_15min_short,
                    term=self.short_term
                )
                ema_15min_long = self.__exponential_moving_average(
                    value=data_15min.loc[i_15min].end,
                    pre_value=ema_15min_long,
                    term=self.long_term
                )
                i_15min += 1
            if i_1min % 5 == 0 and i_1min != 0:
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
                i_5min += 1
            ema_1min_short = self.__exponential_moving_average(
                    value=data_1min.loc[i_1min].end,
                    pre_value=ema_5min_short,
                    term=self.short_term
            )
            ema_1min_long = self.__exponential_moving_average(
                value=data_1min.loc[i_1min].end,
                pre_value=ema_5min_long,
                term=self.long_term
            )
            ema.loc[i_1min + 1] = [
                data_1min.loc[i_1min + 1].end,
                ema_15min_short,
                ema_15min_long,
                ema_5min_short,
                ema_5min_long,
                ema_1min_short,
                ema_1min_long,
                ema_15min_short - ema_15min_long,
                ema_5min_short - ema_5min_long,
                ema_1min_short - ema_1min_long,
                data_1min.loc[i_1min].time,
            ]
        return ema

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
            sma_5min_short,
            sma_5min_long,
            sma_15min_short - sma_15min_long,
            sma_5min_short - sma_5min_long,
            sma_5min_short - sma_5min_long,
            data_5min.loc[0, 'time']
        ]], columns=[
            'price',
            'short_15min',
            'long_15min',
            'short_5min',
            'long_5min',
            'short_1min',
            'long_1min',
            'macd_15min',
            'macd_5min',
            'macd_1min',
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
        data_15min = self.candlestick.loc[::15].reset_index(drop=True)
        data_5min = self.candlestick.loc[::5].reset_index(drop=True)
        return data_15min, data_5min, self.candlestick

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

    def cut_for_ema_1min(self, data_1min):
        """
        SMAで使った部分を切り捨てる
        :param data_1min:
        :return:
        """
        return data_1min[self.long_term * 15:].reset_index(drop=True)
