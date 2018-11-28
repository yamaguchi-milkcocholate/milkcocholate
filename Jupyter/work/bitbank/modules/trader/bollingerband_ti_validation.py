from modules.trader.functions import simple_moving_average
from modules.trader.functions import standard_deviation
from modules.trader.functions import volatility
from modules.datamanager.functions import linear_regression
from modules.datamanager.functions import Polynomial
from modules.fitnessfunction.bollingerband_period_goal_ti import BollingerBandOperationTi
from modules.db.writer import Writer
import numpy as np
import pickle


class BollingerBandValidationTrader:
    """
    BollingerBand, BollingerBandPeriodGoalの取引を想定
    1. インスタンス化
    2. set_genome()で遺伝子をセット
    3. Validationクラスに引き数で渡す
    """
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

    def __init__(self, stock_term, inclination_alpha):
        self.__genome = None
        self.__recent_data = None
        self.__recent_sma = None
        self.__recent_sigma = None
        self.__volatility = None
        self.__has_coin = None
        self.__time = None
        self.__last_location = None
        self.__population_id = None
        self.__stock_term = stock_term
        self.__inclination_alpha = inclination_alpha
        self.__candlestick = None
        self.__update_num = 0

    def set_candlestick(self, candlestick):
        """
        ロウソク足データを受け取って、初期データを計算して準備する関数
        :param candlestick:
        """
        self.__candlestick = candlestick
        self.__initialize()

    def __initialize(self):
        """
        初期データを計算して準備する関数
        """
        self.__recent_data, self.__time = self.dispose_candlestick(
            candlestick=self.__candlestick
        )
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

    def operation(self):
        """
        データを更新して、複数個のシグマと前回、現在の終値の位置から取引の方針を決める
        :return: const int 取引方針を表す定数 / False 取引シミュレーション終了時
        """
        pre_location = self.__last_location
        # 更新するデータがあるかどうかで取引シミュレーションを終了するか続けるかを決める
        if self.__can_update():
            self.fetch_recent_data()
            self.__location()
            inclination_pattern = self.__inclination()
            action = BollingerBandOperationTi.operation(
                last_end_position=pre_location,
                end_position=self.__last_location,
                inclination_pattern=inclination_pattern,
                genome=self.__genome,
                has_bitcoin=self.__has_coin
            )
            return int(action)
        else:
            # 取引シミュレーション終了
            return False

    def fetch_recent_data(self):
        """
        ロウソク足データから次のデータをセットして更新する。更新するデータがなかったらFalseを返してシミュレーション終了
        """
        self.__recent_data, self.__time = self.dispose_candlestick(
            candlestick=self.__candlestick
        )

    def fetch_information(self):
        return self.__recent_data[-1], self.__time

    def dispose_candlestick(self, candlestick):
        """
        テスト用にパブリックフィールドで引き数を持つ。
        ロウソク足データの計算に使う分だけを取り出して返す関数(初回のみ)
        :param candlestick: pandas.DataFrame
        :return:  candlestick_np, time: numpy, string  計算に必要な部分のロウソク足データの終値, 取得時間
        """
        # 単純移動平均線 + 標準偏差 で(期間 - 1) * 2 を余分に使う
        data_size = self.__stock_term * 3 - 2
        candlestick_size = len(candlestick)
        if candlestick_size < data_size:
            raise TypeError('candlestick not have much length', candlestick_size, data_size)
        # DataFrameの終値と時間の列を取り出してnumpyに変換する
        candlestick_np = candlestick.end.values
        # 取り出した
        time = candlestick.at[self.__update_num + data_size, 'time'].strftime('%Y-%m-%d %H:%M:%S')
        # [start:stop:steps] stopは含まれない
        candlestick_np = candlestick_np[self.__update_num:self.__update_num + data_size]
        # データ更新数を増やす
        self.__increment_update_num()
        return candlestick_np, time

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

    def __increment_update_num(self):
        self.__update_num += 1

    def __can_update(self):
        """
        データ更新が可能かをチェックする関数
        :return: bool 可能かどうか
        """
        if len(self.__candlestick) <= (self.__stock_term * 3 - 2 + self.__update_num):
            # データ数が足らない。ロウソク足データを使い切った
            return False
        else:
            # 更新可能
            return True

    def set_genome(self, host, population_id, individual_num=0):
        """
        遺伝子のセッター
        numpyのgenomeかデータベースからのどちらか
        :param host:
        :param population_id:
        :param individual_num: int 個体の番号、初期値は0番のエリート
        """
        self.__population_id = population_id
        population = Writer(host=host).find(
            table='populations',
            search_id=population_id
        )[0]
        genomes = pickle.loads(population['genome'])
        # 個体を選ぶ
        if individual_num >= len(genomes):
            raise TypeError('no individual number')
        self.__genome = genomes[individual_num]

    def get_population_id(self):
        return self.__population_id

    def fetch_has_coin(self, has_coin):
        """
        Validationクラスからコインを持っているかどうかを教えてもらうための関数
        :param has_coin: bool
        """
        self.__has_coin = has_coin
