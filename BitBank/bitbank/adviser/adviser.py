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

    BUY_TYPE = 'buy'
    SELL_TYPE = 'sell'

    def __init__(self, pair='xrp_jpy', candle_type='15min', buying_price=None):
        self.api_gateway = ApiGateway()
        self.pair = pair
        self.candle_type = candle_type
        self.buying_price = buying_price
        self.candlestick = self.make_price_data_frame()

    @abstractmethod
    def operation(self, has_coin, price=None):
        """
        指示と取引価格を渡す。
        :param has_coin: bool
        :param price: None|float
        :return: const int, float
        """
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
        candlestick_today = self.api_gateway.use_candlestick(
            time=today.strftime("%Y%m%d"),
            candle_type=self.candle_type,
            pair=self.pair
        )['candlestick'][0]['ohlcv']
        candlestick_yesterday = self.api_gateway.use_candlestick(
            time=yesterday.strftime('%Y%m%d'),
            candle_type=self.candle_type,
            pair=self.pair
        )['candlestick'][0]['ohlcv']
        for item in candlestick_today:
            candlestick_yesterday.append(item)
        loc = datetime.datetime.fromtimestamp(int(candlestick_yesterday[-1][5]) / 1000)
        print('last: ', loc)
        return pd.DataFrame(candlestick_yesterday, columns=['open', 'high', 'low', 'end', 'yield', 'time'])
