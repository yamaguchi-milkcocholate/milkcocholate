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

    def make_data_frame(self):
        """
        データを作成する
        """
        df_price = self.make_price_data_frame()
        df_15min, df_5min = self.normalize_data_frame(df=df_price)
        df_macd, df_15min, df_5min = self.first_sma_data_frame(df_15min, df_5min)
        df_macd = self.make_macd_data_frame(df_macd, df_5min)
        signal = self.make_signal_data_frame(df_macd)
        return signal

    def make_signal_data_frame(self, df_macd):
        part = df_macd.loc[:self.__signal * 3 - 1]
        sma_15min = float(np.sum(np.unique(part.macd_15min.values)) / self.__signal)
        sma_5min = float(np.sum(part.loc[self.__signal * 2:].macd_5min.values) / self.__signal)
        df_macd = df_macd.loc[self.__signal * 3:].reset_index(drop=True)
        df_signal = pd.DataFrame([[
            part.tail(1).price,
            part.tail(1).macd_15min,
            part.tail(1).macd_5min,
            sma_15min,
            sma_5min,
            part.tail(1).macd_15min - sma_15min,
            part.tail(1).macd_5min - sma_5min,
        ]], columns=[
            'price',
            'macd_15min',
            'macd_5min',
            'signal_15min',
            'signal_5min',
            'histogram_15min',
            'histogram_5min',
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
                df_macd.loc[macd_i].macd_15min,
                df_macd.loc[macd_i].macd_5min,
                signal_15min,
                signal_5min,
                df_macd.loc[macd_i].macd_15min - signal_15min,
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
