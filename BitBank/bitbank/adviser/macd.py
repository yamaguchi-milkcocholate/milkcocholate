from bitbank.apigateway import ApiGateway
import numpy as np
import pandas as pd
from pytz import timezone
import datetime


class MACDAdviser:
    MINUS = -1
    PLUS = 1

    BUY = 1
    STAY = 2
    SELL = 3

    def __init__(self, short_term=12, long_term=26, signal=9, pair='xrp_jpy', candle_type='5min'):
        self.__short_term = short_term
        self.__long_term = long_term
        self.__signal = signal
        self.__pair = pair
        self.__candle_type = candle_type
        self.__api_gateway = ApiGateway()
        self.df_signal = None
        self.make_data_frame()
        self.trend_15min = None
        self.trend_5min = None
        self.area_15min = list()
        self.area_5min = list()
        self.max_histogram_5min = 0
        self.max_histogram_15min = 0
        self.start_macd_15min = None
        self.start_macd_5min = None
        self.start_signal_15min = None
        self.start_signal_5min = None
        self.mount_15min = None
        self.mount_5min = None
        self.count_15min = 1
        self.count_5min = 1
        self.is_plus_start_15min = None
        self.is_plus_start_5min = None
        self.max_price = None
        self.recognize()

    def operation(self, genome, has_coin):
        """
        :return: const integer, float
        """
        # price_rate = genome[28]
        histogram_15min = float(self.df_signal.tail(1).histogram_15min)
        histogram_5min = float(self.df_signal.tail(1).histogram_5min)
        histogram_1min = float(self.df_signal.tail(1).histogram_1min)
        pre_trend_15min = self.trend_15min
        pre_trend_5min = self.trend_5min
        macd_15min = float(self.df_signal.tail(1).macd_15min)
        macd_5min = float(self.df_signal.tail(1).macd_5min)
        macd_1min = float(self.df_signal.tail(1).macd_1min)
        signal_15min = float(self.df_signal.tail(1).signal_15min)
        signal_5min = float(self.df_signal.tail(1).signal_5min)
        signal_1min = float(self.df_signal.tail(1).signal_1min)
        price = float(self.df_signal.tail(1).price)

        self.__check_trend(histogram_15min=histogram_15min, histogram_5min=histogram_1min)
        check_5min = self.__check_5min()

        if check_5min:
            if pre_trend_15min == self.trend_15min:
                self.area_15min.append(histogram_15min)
                if abs(self.max_histogram_15min) < abs(histogram_15min):
                    self.max_histogram_15min = histogram_15min
            else:
                self.area_15min = list()
                self.area_15min.append(histogram_15min)
                self.max_histogram_15min = histogram_15min
                self.start_macd_15min = macd_15min
                self.start_signal_15min = signal_15min
                if has_coin is False and signal_15min > 0:
                    self.is_plus_start_15min = True
                else:
                    self.is_plus_start_15min = False

            if pre_trend_5min == self.trend_5min:
                self.area_5min.append(histogram_1min)
                if abs(self.max_histogram_5min) < abs(histogram_1min):
                    self.max_histogram_5min = histogram_1min
            else:
                self.area_5min = list()
                self.area_5min.append(histogram_1min)
                self.max_histogram_5min = histogram_1min
                self.start_macd_5min = macd_1min
                self.start_signal_5min = signal_1min
                if has_coin is False and signal_1min > 0:
                    self.is_plus_start_5min = True
                else:
                    self.is_plus_start_5min = False
        else:
            if pre_trend_5min == self.trend_5min:
                self.area_5min[-1] = histogram_1min
                if abs(self.max_histogram_5min) < abs(histogram_1min):
                    self.max_histogram_5min = histogram_1min
            else:
                self.area_5min = list()
                self.area_5min.append(histogram_1min)
                self.max_histogram_5min = histogram_1min
                self.start_macd_5min = macd_1min
                self.start_signal_5min = signal_1min
                if has_coin is False and signal_1min > 0:
                    self.is_plus_start_5min = True
                else:
                    self.is_plus_start_5min = False

        # 山が下がり始めたら
        if len(self.area_5min) > 1 and abs(self.area_5min[-1]) > abs(histogram_1min):
            step_size_5min = len(self.area_5min)
            start_decrease_5min = True
        else:
            step_size_5min = None
            start_decrease_5min = False
        if len(self.area_15min) > 1 and abs(self.area_15min[-1]) < abs(self.area_15min[-2]):
            step_size_15min = len(self.area_15min)
            start_decrease_15min = True
        else:
            step_size_15min = None
            start_decrease_15min = False

        if start_decrease_5min and start_decrease_15min:

            if not has_coin and self.is_plus_start_15min and self.is_plus_start_5min:
                decrease_rate_15min = genome[0]
                step_rate_15min = genome[1]
                decrease_rate_5min = genome[2]
                step_rate_5min = genome[3]
                start_macd_15min = genome[4]
                start_signal_15min = genome[5]
                start_macd_5min = genome[6]
                start_signal_5min = genome[7]
                end_macd_15min = genome[8]
                end_signal_15min = genome[9]
                end_macd_5min = genome[10]
                end_signal_5min = genome[11]

                # MAX条件
                max_threshold_5min = step_rate_5min * step_size_5min * self.max_histogram_5min
                max_threshold_5min += start_macd_5min * self.start_macd_5min
                max_threshold_5min += start_signal_5min * self.start_signal_5min
                max_threshold_5min += end_macd_5min * macd_5min
                max_threshold_5min += end_signal_5min * signal_5min
                max_threshold_15min = step_rate_15min * step_size_5min * self.max_histogram_15min
                max_threshold_15min += start_macd_15min * self.start_macd_15min
                max_threshold_15min += start_signal_15min * self.start_signal_15min
                max_threshold_15min += end_macd_15min * macd_15min
                max_threshold_15min += end_signal_15min * signal_15min
                # 降下条件
                decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min
                decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min

                buy = self.and_gate(
                    self.max_histogram_15min < max_threshold_15min,
                    decrease_threshold_15min < histogram_15min,
                    self.max_histogram_5min < max_threshold_5min,
                    decrease_threshold_5min < histogram_1min,
                )
                if buy:
                    operation = self.BUY
                else:
                    operation = self.STAY

            elif has_coin:
                decrease_rate_15min = genome[12]
                step_rate_15min = genome[13]
                decrease_rate_5min = genome[14]
                step_rate_5min = genome[15]
                start_macd_5min = genome[16]
                start_signal_5min = genome[17]
                start_macd_15min = genome[18]
                start_signal_15min = genome[19]
                end_macd_5min = genome[16]
                end_signal_5min = genome[17]
                end_macd_15min = genome[18]
                end_signal_15min = genome[19]

                # MAX条件
                max_threshold_5min = step_rate_5min * step_size_5min * self.max_histogram_5min
                max_threshold_5min += start_macd_5min * self.start_macd_5min
                max_threshold_5min += start_signal_5min * self.start_signal_5min
                max_threshold_5min += end_macd_5min * macd_5min
                max_threshold_5min += end_signal_5min * signal_5min
                max_threshold_15min = step_rate_15min * step_size_15min * self.max_histogram_15min
                max_threshold_15min += start_macd_15min * self.start_macd_15min
                max_threshold_15min += start_signal_15min * self.start_signal_15min
                max_threshold_15min += end_macd_15min * macd_15min
                max_threshold_15min += end_signal_15min * signal_15min
                # 降下条件
                decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min
                decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min

                if not self.max_price:
                    self.max_price = price
                else:
                    if self.max_price < price:
                        self.max_price = price

                sell = self.and_gate(
                    max_threshold_15min < self.max_histogram_15min,
                    histogram_15min < decrease_threshold_15min,
                    max_threshold_5min < self.max_histogram_5min,
                    histogram_1min < decrease_threshold_5min,
                )

                if self.max_price * price_rate > price:
                    sell_price = True
                else:
                    sell_price = False

                if sell or sell_price:
                    operation = self.SELL
                    self.max_price = None
                else:
                    operation = self.STAY
            else:
                operation = self.STAY
        else:
            operation = self.STAY

        return operation, float(self.df_signal.tail(1).price)

    def fetch_recent_data(self):
        """
        現在のtickerのapiを叩いて、最新の取引値を追加してデータを更新する
        """
        ticker = self.__api_gateway.use_ticker(pair=self.__pair)
        ticker = float(ticker['last'])
        tail = self.df_signal.tail(1)

        if self.count_15min == 15:
            self.count_15min = 1
            short_15min = self.__exponential_moving_average(ticker, float(tail.short_15min), self.__short_term)
            long_15min = self.__exponential_moving_average(ticker, float(tail.long_15min), self.__long_term)
            macd_15min = short_15min - long_15min
            signal_15min = self.__exponential_moving_average(macd_15min, float(tail.signal_15min), self.__signal)
            histogram_15min = macd_15min - signal_15min
        else:
            self.count_15min += 1
            short_15min = float(tail.short_15min)
            long_15min = float(tail.long_15min)
            macd_15min = float(tail.macd_15min)
            signal_15min = float(tail.signal_15min)
            histogram_15min = float(tail.histogram_15min)

        check_5min = self.__check_5min()

        if check_5min:
            short_5min = self.__exponential_moving_average(ticker, float(tail.short_5min), self.__short_term)
            long_5min = self.__exponential_moving_average(ticker, float(tail.long_5min), self.__long_term)
            macd_5min = short_5min - long_5min
            signal_5min = self.__exponential_moving_average(macd_5min, float(tail.signal_5min), self.__signal)
            histogram_5min = macd_5min - signal_5min
        else:
            short_5min = float(tail.short_5min)
            long_5min = float(tail.long_5min)
            macd_5min = float(tail.macd_5min)
            signal_5min = float(tail.signal_5min)
            histogram_5min = float(tail.histogram_5min)

        short_1min = self.__exponential_moving_average(ticker, short_5min, self.__short_term)
        long_1min = self.__exponential_moving_average(ticker, long_5min, self.__long_term)
        macd_1min = short_1min - long_1min
        signal_1min = self.__exponential_moving_average(macd_1min, signal_5min, self.__signal)
        histogram_1min = macd_1min - signal_1min

        add = pd.Series([
                ticker,
                short_15min,
                long_15min,
                short_5min,
                long_5min,
                short_1min,
                long_1min,
                macd_15min,
                macd_5min,
                macd_1min,
                signal_15min,
                signal_5min,
                signal_1min,
                histogram_15min,
                histogram_5min,
                histogram_1min
             ], index=[
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
                'signal_15min',
                'signal_5min',
                'signal_1min',
                'histogram_15min',
                'histogram_5min',
                'histogram_1min'
            ],
            name=len(self.df_signal) - 1
        )

        self.df_signal = self.df_signal.append(add)
        self.df_signal = self.df_signal.loc[1:]

    def recognize(self):
        """
        最近の状況を認識する
        """
        size = len(self.df_signal)
        part = self.df_signal.loc[size - 1]
        self.__check_trend(
            histogram_15min=float(part.histogram_15min),
            histogram_5min=float(part.histogram_5min)
        )
        check_macd_15min = False
        pre_macd_15min = float(part.macd_15min)
        iteration = 2
        change_15min = False
        change_5min = False
        while True:
            part = self.df_signal.loc[size - iteration]
            histogram_15min = float(part.histogram_15min)
            histogram_5min = float(part.histogram_5min)
            macd_15min = float(part.macd_15min)
            macd_5min = float(part.macd_5min)
            signal_15min = float(part.signal_15min)
            signal_5min = float(part.signal_5min)

            if pre_macd_15min == macd_15min and check_macd_15min:
                self.count_15min += 1
            else:
                check_macd_15min = True

            pre_trend_15min = self.trend_15min
            pre_trend_5min = self.trend_5min
            self.__check_trend(
                histogram_15min=histogram_15min,
                histogram_5min=histogram_5min
            )

            # 山の終わり
            if pre_trend_15min != self.trend_15min and not change_15min:
                change_15min = True
                self.start_macd_15min = macd_15min
                self.start_signal_15min = signal_15min

            # 山の終わり
            if pre_trend_5min != self.trend_5min and not change_5min:
                change_5min = True
                self.start_macd_5min = macd_5min
                self.start_signal_5min = signal_5min

            if not change_15min:
                self.area_15min.append(histogram_15min)
                if abs(self.max_histogram_15min) < abs(histogram_15min):
                    self.max_histogram_15min = histogram_15min

            if not change_5min:
                self.area_5min.append(histogram_5min)
                if abs(self.max_histogram_5min) < abs(histogram_5min):
                    self.max_histogram_5min = histogram_5min

            if change_5min and change_15min:
                break
            iteration += 1

        self.df_signal = self.df_signal.tail(10).reset_index(drop=True)

    def __check_trend(self, histogram_15min, histogram_5min):
        if histogram_15min >= 0:
            self.trend_15min = self.PLUS
        elif histogram_15min < 0:
            self.trend_15min = self.MINUS
        if histogram_5min >= 0:
            self.trend_5min = self.PLUS
        elif histogram_5min < 0:
            self.trend_5min = self.MINUS

    def __check_5min(self):
        if self.count_5min == 5:
            self.count_5min = 1
            return True
        else:
            self.count_5min += 1
            return False

    def make_data_frame(self):
        """
        データを作成する
        """
        df_price = self.make_price_data_frame()
        df_15min, df_5min = self.normalize_data_frame(df=df_price)
        df_macd, df_15min, df_5min = self.first_sma_data_frame(df_15min, df_5min)
        df_macd = self.make_macd_data_frame(df_macd, df_5min)
        self.df_signal = self.make_signal_data_frame(df_macd)

    def make_signal_data_frame(self, df_macd):
        part = df_macd.loc[:self.__signal * 3 - 1]
        sma_15min = float(np.sum(np.unique(part.macd_15min.values)) / self.__signal)
        sma_5min = float(np.sum(part.loc[self.__signal * 2:].macd_5min.values) / self.__signal)
        df_macd = df_macd.loc[self.__signal * 3:].reset_index(drop=True)
        df_signal = pd.DataFrame([[
            part.tail(1).price,
            part.tail(1).short_15min,
            part.tail(1).long_15min,
            part.tail(1).short_5min,
            part.tail(1).long_5min,
            part.tail(1).short_5min,
            part.tail(1).long_5min,
            part.tail(1).macd_15min,
            part.tail(1).macd_5min,
            part.tail(1).macd_5min,
            sma_15min,
            sma_5min,
            sma_5min,
            part.tail(1).macd_15min - sma_15min,
            part.tail(1).macd_5min - sma_5min,
            part.tail(1).macd_5min - sma_5min,
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
            'signal_15min',
            'signal_5min',
            'signal_1min',
            'histogram_15min',
            'histogram_5min',
            'histogram_1min',
        ])

        signal_15min = sma_15min
        signal_5min = sma_5min
        for macd_i in range(len(df_macd) - 1):
            if macd_i % 3 == 0 and macd_i != 0:
                signal_15min = self.__exponential_moving_average(
                    value=df_macd.loc[macd_i].macd_15min,
                    pre_value=signal_15min,
                    term=self.__signal
                )
            signal_5min = self.__exponential_moving_average(
                value=df_macd.loc[macd_i].macd_5min,
                pre_value=signal_5min,
                term=self.__signal
            )

            df_signal.loc[macd_i + 1] = [
                df_macd.loc[macd_i].price,
                df_macd.loc[macd_i].short_15min,
                df_macd.loc[macd_i].long_15min,
                df_macd.loc[macd_i].short_5min,
                df_macd.loc[macd_i].long_5min,
                df_macd.loc[macd_i].short_5min,
                df_macd.loc[macd_i].long_5min,
                df_macd.loc[macd_i].macd_15min,
                df_macd.loc[macd_i].macd_5min,
                df_macd.loc[macd_i].macd_5min,
                signal_15min,
                signal_5min,
                signal_5min,
                df_macd.loc[macd_i].macd_15min - signal_15min,
                df_macd.loc[macd_i].macd_5min - signal_5min,
                df_macd.loc[macd_i].macd_5min - signal_5min,
            ]
        return df_signal.loc[1:].reset_index(drop=True)

    def make_macd_data_frame(self, df_macd, df_5min):
        ema_15min_short = df_macd.loc[0].short_15min
        ema_15min_long = df_macd.loc[0].long_15min
        ema_5min_short = df_macd.loc[0].short_5min
        ema_5min_long = df_macd.loc[0].long_5min
        for i_5min in range(len(df_5min) - 1):
            if i_5min % 3 == 0 and i_5min != 0:
                ema_15min_short = self.__exponential_moving_average(
                    value=df_5min.loc[i_5min].price,
                    pre_value=ema_15min_short,
                    term=self.__short_term
                )
                ema_15min_long = self.__exponential_moving_average(
                    value=df_5min.loc[i_5min].price,
                    pre_value=ema_15min_long,
                    term=self.__long_term
                )

            ema_5min_short = self.__exponential_moving_average(
                value=df_5min.loc[i_5min].price,
                pre_value=ema_5min_short,
                term=self.__short_term
            )
            ema_5min_long = self.__exponential_moving_average(
                value=df_5min.loc[i_5min].price,
                pre_value=ema_5min_long,
                term=self.__long_term
            )

            df_macd.loc[i_5min + 1] = [
                df_5min.loc[i_5min + 1].price,
                ema_15min_short,
                ema_15min_long,
                ema_5min_short,
                ema_5min_long,
                ema_15min_short - ema_15min_long,
                ema_5min_short - ema_5min_long,
            ]
        return df_macd.loc[1:].reset_index(drop=True)

    def make_price_data_frame(self):
        """
        直近のロウソク足データ(2日分)から終値のデータフレームを作る
        :return: pandas.DataFrame 2日分のロウソク足データ
        """
        today = datetime.datetime.now(timezone('UTC'))
        yesterday = today - datetime.timedelta(days=1)
        today = today.astimezone(timezone('Asia/Tokyo'))
        yesterday = yesterday.astimezone(timezone('Asia/Tokyo'))
        print('Initializing Candlestick Data From',
              today.strftime('%Y-%m-%d'),
              'and',
              yesterday.strftime('%Y-%m-%d')
              )
        candlestick_today = self.__api_gateway.use_candlestick(
            time=today.strftime("%Y%m%d"),
            candle_type=self.__candle_type,
            pair=self.__pair
        )['candlestick'][0]['ohlcv']
        candlestick_yesterday = self.__api_gateway.use_candlestick(
            time=yesterday.strftime('%Y%m%d'),
            candle_type=self.__candle_type,
            pair=self.__pair
        )['candlestick'][0]['ohlcv']
        candlestick_yesterday.extend(candlestick_today)
        candlestick = candlestick_yesterday
        del candlestick_today
        del candlestick_yesterday
        # 終値のみを取り出す
        candlestick = np.asarray(candlestick, dtype=float)
        candlestick = candlestick[0:, 3]
        return pd.DataFrame(candlestick, columns=['price'])

    @staticmethod
    def normalize_data_frame(df):
        """
        終値のデータフレームを15min, 5min, に分けて正規化する
        :param df: pandas.DataFrame
        :return: pandas.DataFrame, pandas.DataFrame
        """
        # 3の倍数に揃える(古いデータを削る)
        df = df.loc[len(df) % 3:]
        df_15min = df.loc[::3].reset_index(drop=True)
        return df_15min, df

    @staticmethod
    def __exponential_moving_average(value, pre_value, term):
        return pre_value + (2 / (term + 1)) * (value - pre_value)

    def first_sma_data_frame(self, df_15min, df_5min):
        """
        :param df_15min:
        :param df_5min:
        :return: ['short_15min', 'long_15min', 'short_5min', 'long_5min''macd_15min', 'macd_5min'], price_15min, price_5min
        """
        sma_15min_short = self.sma_15min_short(df_15min)[0]
        sma_15min_long = self.sma_15min_long(df_15min)[0]
        data_15min = self.cut_for_ema_15min(df_15min)
        sma_5min_short = self.sma_5min_short(df_5min)[0]
        sma_5min_long = self.sma_5min_long(df_5min)[0]
        data_5min = self.cut_for_ema_5min(df_5min)
        ema = pd.DataFrame([[
            data_5min.loc[0].price,
            sma_15min_short,
            sma_15min_long,
            sma_5min_short,
            sma_5min_long,
            sma_15min_short - sma_15min_long,
            sma_5min_short - sma_5min_long,
        ]], columns=[
            'price',
            'short_15min',
            'long_15min',
            'short_5min',
            'long_5min',
            'macd_15min',
            'macd_5min',
        ])
        return ema, data_15min, data_5min

    def sma_15min_short(self, data_15min):
        """
        15minの短期単純移動平均
        :param data_15min:
        :return: SMA, テスト用DataFrame
        """
        part = data_15min.loc[(self.__long_term - self.__short_term):self.__long_term - 1]
        price_sum = np.sum(part.price.values)
        sma = float(price_sum / self.__short_term)
        return sma, part

    def sma_15min_long(self, data_15min):
        """
        15minの長期単純移動平均
        :param data_15min:
        :return: SMA, テスト用DataFrame
        """
        part = data_15min.loc[0: self.__long_term - 1]
        price_sum = np.sum(part.price.values)
        sma = float(price_sum / self.__long_term)
        return sma, part

    def sma_5min_short(self, data_5min):
        """
        5minの短期単純移動平均
        :param data_5min:
        :return: SMA, テスト用のDataFrame
        """
        # 15 = 5 * 3
        part = data_5min.loc[self.__long_term * 3 - self.__short_term:self.__long_term * 3 - 1]
        price_sum = np.sum(part.price.values)
        sma = float(price_sum / self.__short_term)
        return sma, part

    def sma_5min_long(self, data_5min):
        """
        5minの長期単純移動平均
        :param data_5min:
        :return: SMA, テスト用のDataFrame
        """
        # 15 = 5 * 3
        part = data_5min.loc[self.__long_term * 3 - self.__long_term:self.__long_term * 3 - 1]
        price_sum = np.sum(part.price.values)
        sma = float(price_sum / self.__long_term)
        return sma, part

    def cut_for_ema_15min(self, data_15min):
        """
        SMAで使った部分を切り捨てる
        :param data_15min:
        :return:
        """
        return data_15min[self.__long_term:].reset_index(drop=True)

    def cut_for_ema_5min(self, df):
        """
        :param df:
        :return:
        """
        return df[self.__long_term * 3:].reset_index(drop=True)

    @staticmethod
    def and_gate(*args):
        return all(args)
