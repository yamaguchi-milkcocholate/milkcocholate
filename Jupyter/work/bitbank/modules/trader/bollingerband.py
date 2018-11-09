from modules.datamanager.apigateway import ApiGateway
from modules.trader.functions import simple_moving_average
from modules.trader.functions import standard_deviation
from modules.trader.functions import volatility
import datetime
import numpy as np


class BollingerBandTrader:

    def __init__(self, stock_term, candle_type):
        self.__genome = None
        self.__recent_data = None
        self.__recent_sma = None
        self.__recent_sigma = None
        self.__volatility = None
        self.__initialize(candle_type=candle_type)
        self.__stock_term = stock_term
        self.__api_gateway = ApiGateway(pair='btc_jpy')

    def __initialize(self, candle_type):
        """
        直近のデータをロウソク足データの終値で初期化する
        """
        # listで受け取る
        candle_stick = self.__api_gateway.use_candlestick(
            time=datetime.datetime.today().strftime("%Y%m%d"),
            candle_type=candle_type
        )['candlestick'][0]['ohlcv']
        # 計算に使うデータを取り出す
        max_index = len(candle_stick)
        # 単純移動平均線 + 標準偏差 で (期間-1)*2を余分に与える
        data_size = self.__stock_term * 3 - 2
        candle_stick = candle_stick[max_index - data_size:max_index]
        data_list = list()
        # 終値のみを取り出す
        for data_i in range(data_size):
            data_list.append(candle_stick[data_i]['end'])
        # 直近の単純移動平均線を求める
        self.__recent_sma = simple_moving_average(
            data=np.asarray(a=data_list, dtype=np.float32),
            term=self.__stock_term
        )
        # 標準偏差を求める
        self.__recent_sigma = standard_deviation(
            data=self.__recent_sma,
            term=self.__stock_term
        )
        # ボラティリティーを求める
        self.__volatility = volatility(
            sma=self.__recent_sma[-1],
            std=self.__recent_sigma[-1]
        )
        # 直近のデータを期間分だけ残す
        self.__recent_data = np.asarray(
            a=data_list[data_size - self.__stock_term:data_size],
            dtype=np.float32
        )

    def fetch_recent_data(self):
        """
        現在のtickerのapiを叩いて、最新の取引値を追加してデータを更新する
        """
        ticker = self.__api_gateway.use_ticker()['data']['last']
        self.__recent_data.append(ticker)
        self.__recent_data.pop(0)

    def operation(self):
        pass

    def set_genome(self):
        pass
