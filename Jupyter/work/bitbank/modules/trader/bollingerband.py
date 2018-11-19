from modules.datamanager.apigateway import ApiGateway
from modules.trader.functions import simple_moving_average
from modules.trader.functions import standard_deviation
from modules.trader.functions import volatility
from modules.datamanager.functions import linear_regression
from modules.datamanager.functions import Polynomial
from modules.fitnessfunction.bollingerband_linear_end import BollingerBandLinearEndOperation
from modules.db.writer import Writer
import datetime
import numpy as np
import pickle


class BollingerBandTrader:
    UPPER = 0
    UPPER_UPPER = 1
    UPPER_MIDDLE = 2
    MIDDLE_LOWER = 3
    LOWER_LOWER = 4
    LOWER = 5

    POSITIVE_INCLINATION = 1
    NEGATIVE_INCLINATION = -1
    POSITIVE_MIDDLE_INCLINATION = 1.7
    NEGATIVE_MIDDLE_INCLINATION = -1.7

    HYPER_EXPANSION = 0
    EXPANSION = 1
    FLAT = 2
    SQUEEZE = 3
    HYPER_SQUEEZE = 4

    def __init__(self, stock_term, inclination_alpha, candle_type):
        self.__genome = None
        self.__recent_data = None
        self.__recent_sma = None
        self.__recent_sigma = None
        self.__volatility = None
        self.__last_location = None
        self.__population_id = None
        self.__stock_term = stock_term
        self.__inclination_alpha = inclination_alpha
        self.__api_gateway = ApiGateway(pair='btc_jpy')
        self.__initialize(candle_type=candle_type)

    def __initialize(self, candle_type):
        """
        直近のデータをロウソク足データの終値で初期化する
        """
        # listで受け取る
        today = datetime.datetime.today()
        yesterday = today - datetime.timedelta(days=1)
        candlestick_today = self.__api_gateway.use_candlestick(
            time=today.strftime("%Y%m%d"),
            candle_type=candle_type
        )['candlestick'][0]['ohlcv']
        candlestick_yesterday = self.__api_gateway.use_candlestick(
            time=yesterday.strftime('%Y%m%d'),
            candle_type=candle_type
        )['candlestick'][0]['ohlcv']
        candlestick_yesterday.extend(candlestick_today)
        candlestick = candlestick_yesterday
        del candlestick_today
        del candlestick_yesterday
        candlestick = self.dispose_candlestick(
            stock_term=self.__stock_term,
            candlestick=candlestick
        )
        data_list = list()
        # 終値のみを取り出す
        for data_i in range(len(candlestick)):
            # 始値, 高値, 安値, 終値, 出来高, UnixTime
            data_list.append(candlestick[data_i][3])
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
        # 計算に使うデータはnumpyに変換
        self.__recent_data = np.asarray(
            a=data_list,
            dtype=np.int32
        )
        # 終値の位置を求める
        self.__location()

    def __fetch_recent_data(self):
        """
        現在のtickerのapiを叩いて、最新の取引値を追加してデータを更新する
        """
        ticker = self.__api_gateway.use_ticker()
        ticker = ticker['last']
        # データを更新
        np.append(self.__recent_data, ticker)
        np.delete(self.__recent_data, -1)
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
        self.__location()

    @staticmethod
    def dispose_candlestick(stock_term, candlestick):
        """
        テスト用にパブリックフィールドでスタティックフィールド。
        一日のロウソク足データから使うデータのみを取り出す関数
        :param stock_term:
        :param candlestick:
        :return:
        """
        # 単純移動平均線 + 標準偏差 で(期間 - 1) * 2 を余分に使う
        data_size = stock_term * 3 - 2
        candlestick_size = len(candlestick)
        if candlestick_size < data_size:
            raise TypeError('candlestick not  much length', candlestick_size, data_size)
        # [start:stop:steps] stopは含まれない
        return candlestick[candlestick_size - data_size:candlestick_size]

    def operation(self):
        """
        データを更新して、複数個のシグマと前回、現在の終値の位置から取引の方針を決める
        """
        pre_location = self.__last_location
        self.__fetch_recent_data()
        self.__location()
        inclination_pattern = self.__inclination()
        action = BollingerBandLinearEndOperation.operation(
            last_end_position=pre_location,
            end_position=self.__last_location,
            inclination_pattern=inclination_pattern,
            genome=self.__genome
        )
        return int(action)

    def __inclination(self):
        min_sigma = np.amin(self.__recent_sigma)
        # 最小値との差分だけの行列を作る
        t = self.__recent_sigma - np.full_like(a=self.__recent_sigma, fill_value=min_sigma)
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

    def __location(self):
        """
        終値の位置を求める
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

    def set_genome(self, host, population_id):
        """
        遺伝子のセッター
        numpyのgenomeかデータベースからのどちらか
        :param host:
        :param population_id:
        """
        self.__population_id = population_id
        population = Writer(host=host).find(
            table='populations',
            search_id=population_id
        )[0]
        # 一番目のエリート個体を選ぶ
        self.__genome = pickle.loads(population['genome'])[0]

    def get_recent_data(self):
        """
        テスト用のゲッター
        """
        return self.__recent_data

    def get_recent_sma(self):
        """
        テスト用のゲッター
        """
        return self.__recent_sma

    def get_recent_sigma(self):
        """
        テスト用のゲッター
        """
        return self.__recent_sigma

    def get_volatility(self):
        """
        テスト用のゲッター
        """
        return self.__volatility

    def get_genome(self):
        """
        テスト用のゲッター
        """
        return self.__genome

    def get_population_id(self):
        return self.__population_id
