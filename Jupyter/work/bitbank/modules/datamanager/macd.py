import numpy as np
import os
import pandas as pd


class MacD:

    def __init__(self, candlestick, short, long, alpha, signal):
        """

        :param candlestick: DataFrame
        :param short:       int
        :param long:        int
        :param alpha:       float
        :param signal:      int
        """
        self.__candlestick = candlestick
        self.__short = short
        self.__long = long
        self.__alpha = alpha
        self.__signal = signal
        self.__list = []
        self.data = pd.DataFrame([], columns=['end', 'short_term', 'long_term', 'time'])

    def calculate(self):
        columns = ['end', 'short_term', 'long_term', 'time']
        end = self.__long - 1
        short_term_sma = self.__simple_moving_average(self.__candlestick, self.__short, end)
        long_term_sma = self.__simple_moving_average(self.__candlestick, self.__long, end)
        row = self.__candlestick.loc[end]
        self.__append_line([row['end'], short_term_sma, long_term_sma, row['time']], columns)
        pre_line = self.__peek_line()

        for index in range(self.__long, len(self.__candlestick)):
            row = self.__candlestick.loc[index]
            end_value = float(row['end'])
            short_term_ema = self.__exponential_moving_average(end_value, float(pre_line.at[0, 'short_term']), float(2/(self.__short + 1)))
            long_term_ema = self.__exponential_moving_average(end_value, float(pre_line.at[0, 'long_term']), float(2/(self.__long + 1)))
            self.__append_line([end_value, short_term_ema, long_term_ema, row['time']], columns)
            pre_line = self.__peek_line()

        columns = ['end', 'short_term', 'long_term', 'time', 'macd', 'macd_signal']
        for item in self.__list:
            macd = float(item['short_term']) - float(item['long_term'])
            item['macd'] = macd
        self.data = pd.concat(self.__list, ignore_index=True)
        self.__list = []
        end = self.__signal - 1
        macd_signal = self.__simple_moving_average(self.data, self.__signal, end)
        row = self.data.loc[end]
        self.__append_line([row['end'], row['short_term'], row['long_term'], row['time'], row['macd'], macd_signal], columns)
        pre_line = self.__peek_line()
        for index in range(self.__signal, len(self.data)):
            row = self.data.loc[index]
            macd_value = float(row['macd'])
            macd_signal = self.__exponential_moving_average(macd_value, float(pre_line.at[0, 'macd']), float(2/(self.__signal + 1)))
            self.__append_line([row['end'], row['short_term'], row['long_term'], row['time'], macd_value, macd_signal], columns)
            pre_line = self.__peek_line()

        self.data = pd.concat(self.__list, ignore_index=True)
        return self.data

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

    def __append_line(self, array, columns):
        line = pd.DataFrame([array], columns=columns)
        self.__list.append(line)

    def __peek_line(self):
        last = len(self.__list) - 1
        return self.__list[last]

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
