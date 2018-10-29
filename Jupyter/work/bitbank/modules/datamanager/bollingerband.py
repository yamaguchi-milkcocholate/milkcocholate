import pandas as pd
from modules.datamanager import functions


class BollingerBand:

    def __init__(self, candlestick):
        self._candlestick = candlestick
        self._sma_term = None
        self._volatility_term = None
        self._data = None

    def __call__(self, sma_term, std_term):
        """
        :param sma_term: 平均移動線
        :param std_term: 標準偏差
        :return:
        """
        self._sma_term = sma_term
        self._volatility_term = std_term
        self.__calculate()
        return self._data

    def __calculate(self):
        """
        pandas.DataFrame   データ型はfloat32
        columns = ['end', 'lower_band', 'upper_band', 'time']
        """
        sma = functions.simple_moving_average(
            candlestick_end=self._candlestick,
            term=self._sma_term,
        )
        sma_end = pd.DataFrame({
            'end': self._candlestick.tail(len(sma)).end.values,
            'simple_moving_average': sma.simple_moving_average.values
        })
        vol = functions.volatility(
            simple_moving_average_end=sma_end,
            term=self._volatility_term
        )
        self._data = pd.DataFrame({
            'end': self._candlestick.tail(len(vol)).end.values,
            'lower_band': vol.lower_band.values,
            'upper_band': vol.upper_band.values,
            'lower_band_double': vol.lower_band_double.values,
            'upper_band_double': vol.upper_band_double.values,
            'sigma': vol.sigma.values,
            'time': self._candlestick.tail(len(vol)).time.values
        })


