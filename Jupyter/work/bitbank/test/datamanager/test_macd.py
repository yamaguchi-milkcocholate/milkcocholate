import os
import sys
import unittest
import pandas as pd
sys.path.append(os.pardir + '/../')
from modules.datamanager.macd import MACD


class TestMACD(unittest.TestCase):

    def setUp(self):
        self.macd = MACD()
        self.macd.short_term = 12
        self.macd.long_term = 26
        self.macd.candlestick = self.sample_data()
        self.data_15min, self.data_5min, self.data_1min = self.macd.normalize_data()

    def tearDown(self):
        pass

    def test_sma_15min_short(self):
        sma, result = self.macd.sma_15min_short(self.data_15min)
        self.assertEqual(12, len(result))
        self.assertEqual(1, sma)

    def test_sma_15min_long(self):
        sma, result = self.macd.sma_15min_long(self.data_15min)
        self.assertEqual(26, len(result))
        self.assertEqual(1, sma)

    def test_sma_5min_short(self):
        sma, result = self.macd.sma_5min_short(self.data_5min)
        self.assertEqual(12, len(result))
        self.assertEqual(1, sma)

    def test_sma_5min_long(self):
        sma, result = self.macd.sma_5min_long(self.data_5min)
        self.assertEqual(26, len(result))
        self.assertEqual(1, sma)

    def test_first_sma_data_frame(self):
        ema = self.macd.first_sma_data_frame(self.data_15min, self.data_5min)

    def test_normalize_data(self):
        self.macd.normalize_data()

    def test_call(self):
        self.macd()

    @staticmethod
    def sample_data():
        df_list = list()
        for i in range(420):
            df_list.append([1, 'time'])
        return pd.DataFrame(df_list, columns=['end', 'time'])


if __name__ == '__main__':
    unittest.main()
