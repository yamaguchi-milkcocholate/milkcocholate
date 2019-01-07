from bitbank.apigateway import ApiGateway
import pandas as pd
from pytz import timezone
import datetime


class ZigZagAdviser:
    BUY = 1
    STAY = 2
    SELL = 3

    TOP = 10
    BOTTOM = 11
    OTHER = 12

    def __init__(self, pair='xrp_jpy', candle_type='15min'):
        self.__pair = pair
        self.__candle_type = candle_type
        self.__api_gateway = ApiGateway()
        self.genome = None
        self.depth = None
        self.deviation = None
        self.max_high = None
        self.min_low = None
        self.max_high_i = None
        self.min_low_i = None
        self.top_i = None
        self.bottom_i = None
        self.last_depth = None
        self.data_i = None
        self.price = None
        self.trend = None
        self.candlestick = self.make_price_data_frame()

    def __call__(self, *args, **kwargs):
        self.zigzag_candlestick()
        self.candlestick = None

    def operation(self, has_coin):
        # 売りのエントリー
        if self.trend == self.TOP and has_coin:
            operation = self.SELL
            return operation, self.price

        # 買いのエントリー
        elif self.trend == self.BOTTOM and not has_coin:
            operation = self.BUY
            return operation, self.price

        elif self.trend == self.OTHER:
            operation = self.STAY
            return operation, self.price

    def fetch_recent_data(self):
        """
        現在のtickerのapiを叩いて、最新の取引値を追加してデータを更新する
        """
        self.data_i += 1
        ticker = self.__api_gateway.use_ticker(pair=self.__pair)
        ticker = float(ticker['last'])
        self.__update_min_max(high=ticker, low=ticker, i=self.data_i)
        self.price = ticker

        self.__trend()

    def zigzag_candlestick(self):
        self.max_high = float(self.candlestick.loc[0].high)
        self.min_low = float(self.candlestick.loc[0].low)
        self.max_high_i = 0
        self.min_low_i = 0
        self.top_i = 0
        self.bottom_i = 0
        self.last_depth = 10**3   # 適当な大きさ

        for data_i in range(1, len(self.candlestick)):
            self.data_i = data_i
            high = float(self.candlestick.loc[data_i].high)
            low = float(self.candlestick.loc[data_i].low)

            self.__update_min_max(high=high, low=low, i=data_i)

            self.__trend(high=high, low=low)

    def __update_min_max(self, high, low, i):
        if self.max_high < high:
            self.max_high = high
            self.max_high_i = i
        if self.min_low > low:
            self.min_low = low
            self.min_low_i = i

    def __top(self):
        return self.__and_gate(
            self.min_low * (1 + self.deviation) < self.max_high,
            self.min_low_i < self.max_high_i,
            self.last_depth + (self.max_high_i - self.bottom_i) > self.depth
        )

    def __bottom(self):
        return self.__and_gate(
            self.max_high * (1 - self.deviation) > self.min_low,
            self.max_high_i < self.min_low_i,
            self.last_depth + (self.min_low_i - self.top_i) > self.depth
        )

    def __trend(self, high=None, low=None):
        if not high:
            high = self.price
        if not low:
            low = self.price
        if self.__top():
            self.last_depth = self.data_i - self.bottom_i
            self.top_i = self.data_i
            self.min_low = low
            self.min_low_i = self.data_i
            self.trend = self.TOP

        elif self.__bottom():
            self.last_depth = self.data_i - self.top_i
            self.bottom_i = self.data_i
            self.max_high = high
            self.max_high_i = self.data_i
            self.trend = self.BOTTOM

        else:
            self.trend = self.OTHER

    def __depth_bias(self):
        """
        15分足と30秒足に変換
        """
        self.last_depth *= 30
        self.depth *= 30

    @staticmethod
    def __and_gate(*args):
        return all(args)

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
        for item in candlestick_today:
            candlestick_yesterday.append(item)
        return pd.DataFrame(candlestick_yesterday, columns=['open', 'high', 'low', 'end', 'yield', 'time'])

    def set_genome(self, genome):
        self.genome = genome
        print(genome)
        self.depth = genome[0]
        self.deviation = genome[1]
