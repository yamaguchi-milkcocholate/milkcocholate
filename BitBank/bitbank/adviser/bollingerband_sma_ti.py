from bitbank.apigateway import ApiGateway
from bitbank.adviser.functions import simple_moving_average
from bitbank.adviser.functions import standard_deviation
from bitbank.adviser.functions import volatility
from bitbank.adviser.functions import linear_regression
from bitbank.adviser.functions import Polynomial
import numpy as np
from pytz import timezone
import datetime


class BollingerBandSMATiAdviser:
    """
    BollingerBandSMATiの内容にしたがって売買の指示を出す
    """
    UPPER = 0
    UPPER_UPPER = 1
    UPPER_MIDDLE = 2
    MIDDLE_LOWER = 3
    LOWER_LOWER = 4
    LOWER = 5

    POSITIVE_INCLINATION = 1.376
    NEGATIVE_INCLINATION = -1.376
    POSITIVE_MIDDLE_INCLINATION = 0.325
    NEGATIVE_MIDDLE_INCLINATION = -0.325

    HYPER_EXPANSION = 0
    EXPANSION = 1
    FLAT = 2
    SQUEEZE = 3
    HYPER_SQUEEZE = 4

    def __init__(self, stock_term, inclination_alpha, pair, candle_type='5min'):
        self.__recent_data = None
        self.__recent_sma = None
        self.__recent_sigma = None
        self.__volatility = None
        self.__last_location = None
        self.__pre_location = None
        self.__inclination_pattern = None
        self.__stock_term = stock_term
        self.__inclination_alpha = inclination_alpha
        self.__pair = pair
        self.__candle_type = candle_type
        self.__api_gateway = ApiGateway()
        self.__initialize()

    def __initialize(self):
        """
        直近のロウソク足データの終値でで初期化する
        """
        # 直近のロウソク足データを読み込む
        candlestick = self.__fetch_recent_candlestick()

        # 必要な分のロウソク足データのみを切り取る
        candlestick = self.slice_off_candlestick(
            candlestick=candlestick
        )

        # ロウソク足データの終値のみを取り出す
        data_list = list()
        for data_i in range(len(candlestick)):
            # 始値, 高値, 安値, 終値, 出来高, UnixTime
            data_list.append(candlestick[data_i][3])

        # データを使って計算する
        # 直近の単純移動平均線を求める
        self.__recent_sma = simple_moving_average(
            data=np.asarray(a=data_list, dtype=np.float32),
            term=self.__stock_term
        )
        print(self.__recent_sma)
        # 標準偏差を求める(1値)
        self.__recent_sigma = standard_deviation(
            data=self.__recent_sma,
            term=self.__stock_term
        )
        print(self.__recent_sigma)

        # ボラティリティーを求める
        self.__volatility = volatility(
            sma=self.__recent_sma[-1],
            std=self.__recent_sigma[-1]
        )
        # 計算に使うデータはnumpyに変換
        self.__recent_data = np.asarray(
            a=data_list,
            dtype=np.float32
        )
        # 終値の位置を求める
        self.__location()

    def fetch_recent_data(self):
        """
        現在のtickerのapiを叩いて、最新の取引値を追加してデータを更新する
        """
        ticker = self.__api_gateway.use_ticker(pair=self.__pair)
        ticker = float(ticker['last'])

        # データを更新
        self.__recent_data = np.append(self.__recent_data, ticker)
        self.__recent_data = np.delete(self.__recent_data, 0)

        # 直近の単純移動平均線を求める
        self.__recent_sma = simple_moving_average(
            data=np.asarray(a=self.__recent_data, dtype=np.float32),
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
        # 終値の位置を求める
        self.__pre_location = self.__last_location
        self.__location()

    def __inclination(self):
        """
        単純移動平均の1次線形回帰
        :return: 傾きのパターン
        """
        recent_sma = self.__recent_sma[
                     len(self.__recent_sma) - self.__stock_term:len(self.__recent_sma)
                     ]
        print(len(self.__stock_term), len(recent_sma))
        min_sma = np.amin(recent_sma)
        # 最小値との差分だけの行列を作る
        t = recent_sma - np.full_like(a=recent_sma, fill_value=min_sma)
        t = t * 1000
        x = np.arange(
            start=0,
            step=self.__inclination_alpha,
            stop=self.__inclination_alpha * len(t)
        )
        # 直線(１次多項式)の線形回帰
        # その傾きを取り出す
        inclination = linear_regression(
            x=x,
            t=t,
            basic_function=Polynomial(dim=2)
        )[1]
        print('inclination: ' + str(inclination))

        if self.POSITIVE_INCLINATION < inclination:
            inclination_pattern = self.HYPER_EXPANSION
        elif (self.POSITIVE_MIDDLE_INCLINATION < inclination) and (inclination <= self.POSITIVE_INCLINATION):
            inclination_pattern = self.EXPANSION
        elif (self.NEGATIVE_MIDDLE_INCLINATION <= inclination) and (inclination <= self.POSITIVE_MIDDLE_INCLINATION):
            inclination_pattern = self.FLAT
        elif (self.NEGATIVE_INCLINATION <= inclination) and (inclination < self.NEGATIVE_MIDDLE_INCLINATION):
            inclination_pattern = self.SQUEEZE
        elif inclination < self.NEGATIVE_INCLINATION:
            inclination_pattern = self.HYPER_SQUEEZE
        else:
            raise TypeError('inclination is None')
        return inclination_pattern

    def slice_off_candlestick(self, candlestick):
        """
        与えられたロウソク足データの必要な部分だけを切り取って返す関数
        :param candlestick: list ロウソク足データ
        :return: list
        """
        # 単純移動平均線 + 標準偏差 で(期間 - 1) * 1 を余分に使う
        data_size = self.__stock_term * 2 - 1
        candlestick_size = len(candlestick)
        if candlestick_size < data_size:
            raise TypeError('candlestick not have much length', candlestick_size, data_size)
        # [start:stop:steps] stopは含まれない
        return candlestick[candlestick_size - data_size:candlestick_size]

    def __fetch_recent_candlestick(self):
        """
        直近のロウソク足データを2日分読み込む
        :return: list 2日分のロウソク足データ
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
        return candlestick

    def __location(self):
        """
        価格の位置を求める
        """
        end_price = self.__recent_data[-1]
        if self.__volatility['double_upper'] < end_price:
            self.__last_location = self.UPPER
        elif (self.__volatility['upper'] < end_price) and (end_price <= self.__volatility['double_upper']):
            self.__last_location = self.UPPER_UPPER
        elif (self.__volatility['sma'] < end_price) and (end_price <= self.__volatility['upper']):
            self.__last_location = self.UPPER_MIDDLE
        elif (self.__volatility['lower'] <= end_price) and (end_price <= self.__volatility['sma']):
            self.__last_location = self.MIDDLE_LOWER
        elif (self.__volatility['double_lower'] <= end_price) and (end_price < self.__volatility['lower']):
            self.__last_location = self.LOWER_LOWER
        elif end_price < self.__volatility['double_lower']:
            self.__last_location = self.LOWER
        else:
            raise TypeError()

    def operation(self, genome, has_coin):
        """
         データを更新して、複数個のシグマと前回、現在の終値の位置から取引の方針を決める
        :param genome:
        :param has_coin:
        :return: const int 取引方針をあらわす定数, float 最新の価格
        """
        self.__inclination_pattern = self.__inclination()
        action = self.determine_action(
            genome=genome,
            has_coin=has_coin
        )
        return action, self.__recent_data[-1]

    def determine_action(self, genome, has_coin):
        """
        終値、上部バンド、下部バンドから(買い,売り,保持)を決める
        ※ 遺伝子の特徴
        [(前回の終値位置0~5 * 1)(現在の終値位置0~5 * 6)(傾きのパターン0~4 * 36)(ビットコインを持っているか0~1 * 180)]
        """
        if has_coin:
            has_coin = 1
        else:
            has_coin = 0
        return genome[self.__pre_location * 1 + self.__last_location * 6 + self.__inclination_pattern * 36 + has_coin * 180]

    def get_recent_data(self):
        """
        テスト用のゲッター
        :return: numpy
        """
        return self.__recent_data
