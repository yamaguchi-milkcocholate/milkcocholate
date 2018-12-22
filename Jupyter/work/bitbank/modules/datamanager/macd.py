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
        self.__list = None
        self.data = None

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
        self.__list = []
        columns = ['price', '15min', '5min', '1min', 'time']
        self.data = pd.DataFrame([], columns=columns)
        self.calculate()
        return self.data

    def calculate(self):
        """
        15min       EMA
        5min        EMA
        1min + 5min EMA
        """
        data_15min, data_5min = self.normalize_data()
        sma = self.fitst_sma(data_15min, data_5min)
        columns = ['end', 'short_term', 'long_term', 'time']
        line = self.__new_first_line()
        self.__append_line(line, columns)
        pre_line = self.__peek_line()

        for index in range(self.long_term, len(self.candlestick)):
            line = self.__new_following_line(index, pre_line)
            self.__append_line(line, columns)
            pre_line = self.__peek_line()

        columns = ['end', 'short_term', 'long_term', 'time', 'macd', 'macd_signal']
        for item in self.__list:
            macd = float(item['short_term']) - float(item['long_term'])
            item['macd'] = macd

        self.__replace_line_to_data_frame()

        line = self.__extend_first_line()
        self.__append_line(line, columns)
        pre_line = self.__peek_line()

        for index in range(self.signal, len(self.data)):
            line = self.__extend_following_line(index, pre_line)
            self.__append_line(line, columns)
            pre_line = self.__peek_line()

        self.__replace_line_to_data_frame()

    def first_sma(self, data_15min, data_5min):
        """
        最初は単純移動平均
        :param data_15min: pandas.DataFrame
        :param data_5min: pandas.DataFrame
        :return: pandas.DataFrame, pandas.DataFrame
        ['15min_short', '15min_long', '5min_short', '5min_long', 'price'], candlestick
        """
        sma_15min_short = self.sma_15min_short(data_15min)
        sma_15min_long = self.sma_15min_long(data_15min)
        data_15min = self.cut_for_ema_15min(data_15min)
        sma_5min_short = self.sma_5min_short(data_5min)
        sma_5min_long = self.sma_5min_long(data_5min)
        data_5min = self.cut_for_ema_5min(data_5min)

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
        self.data = self.data.loc[0:len(self.data) - len(self.data) % 15 - 1]
        data_15min = self.data.loc[::15].reset_index(drop=True)
        data_5min = self.data.loc[::5].reset_index(drop=True)
        return data_15min, data_5min

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

    def __new_first_line(self):
        end = self.long_term - 1
        short_term_sma = self.__simple_moving_average(self.candlestick, self.short_term, end)
        long_term_sma = self.__simple_moving_average(self.candlestick, self.long_term, end)
        row = self.candlestick.loc[end]
        return [row['end'], short_term_sma, long_term_sma, row['time']]

    def __new_following_line(self, index, pre_line):
        row = self.candlestick.loc[index]
        end_value = float(row['end'])
        short_term_ema = self.__exponential_moving_average(end_value, float(pre_line.at[0, 'short_term']),
                                                           float(2 / (self.short_term + 1)))
        long_term_ema = self.__exponential_moving_average(end_value, float(pre_line.at[0, 'long_term']),
                                                          float(2 / (self.long_term + 1)))
        return [end_value, short_term_ema, long_term_ema, row['time']]

    def __replace_line_to_data_frame(self):
        self.data = pd.concat(self.__list, ignore_index=True)
        self.__list = []

    def __extend_first_line(self):
        end = self.signal - 1
        macd_signal = self.__simple_moving_average(self.data, self.signal, end)
        row = self.data.loc[end]
        return [row['end'], row['short_term'], row['long_term'], row['time'], row['macd'], macd_signal]

    def __extend_following_line(self, index, pre_line):
        row = self.data.loc[index]
        macd_value = float(row['macd'])
        macd_signal = self.__exponential_moving_average(macd_value, float(pre_line.at[0, 'macd']),
                                                        float(2 / (self.signal + 1)))
        return [row['end'], row['short_term'], row['long_term'], row['time'], macd_value, macd_signal]

    @staticmethod
    def __simple_moving_average(df, span, end):
        """
        :param df:
        :param span:
        :param end: int index of the end day
        :return:
        """
        wa = 0
        start = end - span + 1
        part = df.loc[start:end]
        for index, row in part.iterrows():
            wa += int(row['end'])
        return float(wa / span)

    @staticmethod
    def __exponential_moving_average(value, pre_value, alpha):
        return pre_value + alpha * (value - pre_value)

    @staticmethod
    def __calc_simple_mean(df, span, end):
        """
        :param df:
        :param span:
        :param end: int index of the end day
        :return:
        """
        wa = 0
        start = end - span + 1
        part = df.loc[start:end]
        for index, row in part.iterrows():
            wa += int(row['end'])
        return float(wa/span)

    def __append_line(self, array, columns):
        line = pd.DataFrame([array], columns=columns)
        self.__list.append(line)

    def __peek_line(self):
        last = len(self.__list) - 1
        return self.__list[last]
