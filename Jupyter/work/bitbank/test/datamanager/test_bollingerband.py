import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from modules.datamanager import bollingerband
from modules.datamanager import picker


class TestBollingerBand(unittest.TestCase):

    def setUp(self):
        candlestick = picker.Picker('1hour').get_candlestick()
        self._bollinger_band = bollingerband.BollingerBand(
            candlestick=candlestick
        )

    def test_bollinger_band(self):
        data = self._bollinger_band(
            sma_term=10,
            volatility_term=10
        )
        print(data)
        # pandas.DataFrame データ型はfloat32
        print(data.dtypes)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
