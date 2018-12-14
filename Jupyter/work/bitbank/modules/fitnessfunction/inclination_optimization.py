from modules.datamanager.bollingerband import BollingerBand
from modules.datamanager import functions
from modules.datamanager.picker import Picker
import matplotlib.pyplot as plt
import numpy as np


class InclinationOptimization:
    POSITIVE_INCLINATION = 1.376
    NEGATIVE_INCLINATION = -1.376
    POSITIVE_MIDDLE_INCLINATION = 0.325
    NEGATIVE_MIDDLE_INCLINATION = -0.325

    def __init__(self, sma_term, std_term, stock_term, inclination_alpha, candle_type='5min', target='sigma', data_set=True):
        self.__candlestick = Picker(
            candle_type,
            use_of_data='training',
            coin='xrp',
            is_inclination=data_set
        ).get_candlestick()
        self.__approach = BollingerBand(
            candlestick=self.__candlestick
        )
        self.__data = self.__approach(
            sma_term=sma_term,
            std_term=std_term
        )
        self.__stock_term = stock_term
        self.__inclination_alpha = inclination_alpha
        self.__target = target
        self.__inclination_check = None
        self.__inclination_list = list()
        self.__inclination_init()

    def __call__(self):
        for data_i in range(self.__stock_term - 1, len(self.__data)):
            self.inclination(data_i=data_i)
        self.__inclination_init()
        self.__plot()
    
    def __inclination_init(self):
        if self.__inclination_check is not None:
            print(self.__inclination_check)
        self.__inclination_check = [0, 0, 0, 0, 0]
    
    def inclination(self, data_i):
        """
        標準偏差の傾きを調べる。ボラティリティの広がりをパターンに分ける
        :param data_i: 
        :return: 
        """
        pre_data = self.__data.loc[data_i - self.__stock_term + 1:data_i, self.__target].values
        min_price = np.amin(pre_data)
        t = pre_data - np.full_like(a=pre_data, fill_value=min_price)
        t = t * 1000
        x = np.arange(
            start=0,
            step=self.__inclination_alpha,
            stop=self.__inclination_alpha * len(t)
        )
        inclination = functions.linear_regression(
            x=x,
            t=t,
            basic_function=functions.Polynomial(dim=2)
        )[1]
        self.__inclination_list.append(inclination)
        self.inclination_pattern(inclination=inclination)

    def inclination_pattern(self, inclination):
        if self.POSITIVE_INCLINATION < inclination:
            self.__inclination_check[0] += 1
        elif (self.POSITIVE_MIDDLE_INCLINATION < inclination) and (inclination <= self.POSITIVE_INCLINATION):
            self.__inclination_check[1] += 1
        elif (self.NEGATIVE_MIDDLE_INCLINATION <= inclination) and (inclination <= self.POSITIVE_MIDDLE_INCLINATION):
            self.__inclination_check[2] += 1
        elif (self.NEGATIVE_INCLINATION <= inclination) and (inclination < self.NEGATIVE_MIDDLE_INCLINATION):
            self.__inclination_check[3] += 1
        elif inclination < self.NEGATIVE_INCLINATION:
            self.__inclination_check[4] += 1
        else:
            pass

    def get_inclination_check(self):
        return self.__inclination_check

    def __plot(self):
        height = np.asarray(self.__inclination_list)
        height.sort()
        left = np.arange(1, len(height) + 1)
        plt.bar(left, height)
        plt.show()
