import pandas as pd


class MacD:

    def __init__(self, candlestick):
        self.candlestick = candlestick
        self.short_term = None
        self.long_term = None
        self.signal = None
        self.__list = None
        self.data = None

    def __call__(self, short_term, long_term, signal):
        """
        :param short-term:       int
        :param long-term:        int
          :param signal:         int
        """
        self.short_term = short_term
        self.long_term = long_term
        self.signal = signal
        self.__list = []
        self.data = pd.DataFrame([], columns=['end', 'short_term', 'long_term', 'time'])
        self.calculate()
        return self.data

    def calculate(self):
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
