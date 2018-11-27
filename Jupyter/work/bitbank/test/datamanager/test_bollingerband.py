import os
import sys
import unittest
import numpy as np
sys.path.append(os.pardir + '/../')
from modules.datamanager import bollingerband
from modules.datamanager import picker


class TestBollingerBand(unittest.TestCase):

    def setUp(self):
        self._candlestick = picker.Picker('1hour', use_of_data='training', pair='btc').get_candlestick()
        self._bollinger_band = bollingerband.BollingerBand(
            candlestick=self._candlestick
        )

    def test_bollinger_band(self):
        data = self._bollinger_band(
            sma_term=10,
        )
        # print(data)
        # pandas.DataFrame データ型はfloat32
        print(data.dtypes)
        self.assertEqual(len(self._candlestick), len(data) + 9 + 9)
        self.assertEqual(data.dtypes.end, np.float32)
        self.assertEqual(data.dtypes.upper_band, np.float32)
        self.assertEqual(data.dtypes.lower_band, np.float32)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
