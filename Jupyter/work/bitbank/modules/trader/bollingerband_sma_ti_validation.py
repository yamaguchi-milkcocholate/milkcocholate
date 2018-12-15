from modules.datamanager.functions import linear_regression
from modules.datamanager.functions import Polynomial
from modules.db.writer import Writer
from modules.fitnessfunction.bollingerband_period_goal_ti import BollingerBandOperationTi
from modules.datamanager.bollingerband import BollingerBand
import numpy as np
import pickle


class BollingerBandSMATiValidationTrader:
    """
    BollingerBandSMATiの取引を想定
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

    POSITIVE_INCLINATION = 1.376
    NEGATIVE_INCLINATION = -1.376
    POSITIVE_MIDDLE_INCLINATION = 0.325
    NEGATIVE_MIDDLE_INCLINATION = -0.325

    HYPER_EXPANSION = 0
    EXPANSION = 1
    FLAT = 2
    SQUEEZE = 3
    HYPER_SQUEEZE = 4

    def __init__(self, stock_term, inclination_alpha):
        self.__data = None
        self.__has_coin = None
        self.__genome = None
        self.__population_id = None
        self.__last_location = None
        self.__time = None
        self.__price = None
        self.__stock_term = stock_term
        self.__inclination_alpha = inclination_alpha
        self.__iteration = 1

    def set_candlestick(self, candlestick):
        """
        ロウソク足データを受け取って、初期データを計算して準備する関数
        :param candlestick:
        """
        bollingerband = BollingerBand(candlestick=candlestick)
        self.__data = bollingerband(
            sma_term=self.__stock_term,
            std_term=self.__stock_term
        )
        self.__location(volatility=self.__data.loc[self.__stock_term])

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

    def operation(self):
        """
        データを更新して、複数個のシグマと前回、現在の終値の位置から取引の方針を決める
        :return: const int 取引方針を表す定数 / False 取引シミュレーション終了時
        """
        if (self.__iteration + self.__stock_term) < len(self.__data):
            pre_location = self.__last_location
            volatility = self.__data.loc[self.__iteration + self.__stock_term]
            self.__location(volatility=volatility)

            sma = self.__data.loc[self.__iteration:self.__iteration + self.__stock_term].simple_moving_average
            inclination_pattern = self.__inclination(sma=sma)

            action = BollingerBandOperationTi.operation(
                last_end_position=pre_location,
                end_position=self.__last_location,
                inclination_pattern=inclination_pattern,
                genome=self.__genome,
                has_bitcoin=self.__has_coin
            )
            self.__iteration += 1
            return int(action)
        else:
            return False

    def __location(self, volatility):
        """
        終値の位置を求める
        """
        end_price = volatility.end
        self.__price = end_price
        self.__time = volatility.time
        if volatility.upper_band_double < end_price:
            self.__last_location = self.UPPER
        elif (volatility.upper_band < end_price) and (end_price <= volatility.upper_band_double):
            self.__last_location = self.UPPER_UPPER
        elif (volatility.simple_moving_average < end_price) and (end_price <= volatility.upper_band):
            self.__last_location = self.UPPER_MIDDLE
        elif (volatility.lower_band <= end_price) and (end_price <= volatility.simple_moving_average):
            self.__last_location = self.MIDDLE_LOWER
        elif (volatility.lower_band_double <= end_price) and (end_price < volatility.lower_band):
            self.__last_location = self.LOWER_LOWER
        elif end_price < volatility.lower_band_double:
            self.__last_location = self.LOWER
        else:
            raise TypeError()

    def __inclination(self, sma):
        sma_np = sma.astype(np.float64)
        min_sigma = np.amin(sma_np)
        # 最小値との差分だけの行列を作る
        t = sma_np - np.full_like(a=sma_np, fill_value=min_sigma)
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

    def fetch_information(self):
        return self.__price, self.__time
