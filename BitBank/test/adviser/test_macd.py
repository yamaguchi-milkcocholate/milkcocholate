import os
import sys
import unittest
import pandas as pd
sys.path.append(os.pardir + '/../')
from bitbank.adviser.macd import MACDAdviser


class TestMACDAdviser(unittest.TestCase):

    def setUp(self):
        self.adviser = MACDAdviser()
        self.short_term = 12
        self.long_term = 26

    def test_macd(self):
        # price
        result = self.adviser.make_price_data_frame()
        self.assertIsInstance(result, pd.DataFrame)
        # DataFrame(price)
        df_15min, df_5min = self.adviser.normalize_data_frame(df=result)
        self.assertEqual(len(df_15min) * 3, len(df_5min))
        self.assertEqual(float(df_15min.tail(1).price), float(df_15min.tail(1).price))
        self.assertEqual(float(df_15min.head(1).price), float(df_15min.head(1).price))
        # 5min
        short_5min, part_1 = self.adviser.sma_5min_short(df_5min)
        self.assertEqual(len(part_1), self.short_term)
        long_5min, part_2 = self.adviser.sma_5min_long(df_5min)
        self.assertEqual(len(part_2), self.long_term)
        cut_5min = self.adviser.cut_for_ema_5min(df_5min)
        self.assertEqual(len(cut_5min), len(df_5min) - self.long_term * 3)
        # 15min
        short_15min, part_1 = self.adviser.sma_15min_short(df_15min)
        self.assertEqual(len(part_1), self.short_term)
        long_15min, part_2 = self.adviser.sma_15min_long(df_15min)
        self.assertEqual(len(part_2), self.long_term)
        cut_15min = self.adviser.cut_for_ema_15min(df_15min)
        self.assertEqual(len(cut_15min), len(df_15min) - self.long_term)
        # macd first
        df_macd, df_15min, df_5min = self.adviser.first_sma_data_frame(df_15min, df_5min)
        # macd rest
        df_macd = self.adviser.make_macd_data_frame(df_macd, df_5min)
        self.assertEqual(len(df_macd), len(df_5min) - 1)
        self.assertEqual(float(df_macd.tail(1).price), float(df_5min.tail(1).price))
        df_signal = self.adviser.make_signal_data_frame(df_macd)
        self.assertEqual(float(df_signal.tail(1).price), float(df_macd.tail(2).reset_index(drop=True).loc[0].price))


if __name__ == '__main__':
    unittest.main()
