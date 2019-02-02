from abc import ABC, abstractmethod
from bitbank.apigateway import ApiGateway
from pytz import timezone
import datetime
import pandas as pd


class Adviser(ABC):
    BUY = 1
    STAY = 2
    SELL = 3
    RETRY = 4

    def __init__(self, pair='xrp_jpy'):
        self.api_gateway = ApiGateway()
        self.pair = pair

    def __call__(self, *args, **kwargs):
        pass

    @abstractmethod
    def operation(self, has_coin):
        """
        指示と取引価格を渡す。
        :param has_coin: bool
        :return: const int, float
        """
        pass

    @abstractmethod
    def fetch_recent_data(self):
        pass

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
        candlestick_today = self.api_gateway.use_candlestick(
            time=today.strftime("%Y%m%d"),
            candle_type=self.api_gateway,
            pair=self.pair
        )['candlestick'][0]['ohlcv']
        candlestick_yesterday = self.api_gateway.use_candlestick(
            time=yesterday.strftime('%Y%m%d'),
            candle_type=self.api_gateway,
            pair=self.pair
        )['candlestick'][0]['ohlcv']
        for item in candlestick_today:
            candlestick_yesterday.append(item)
        return pd.DataFrame(candlestick_yesterday, columns=['open', 'high', 'low', 'end', 'yield', 'time'])

