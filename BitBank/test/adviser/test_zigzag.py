import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from bitbank.adviser.zigzag import ZigZagAdviser


class TestZigZag(unittest.TestCase):

    def setUp(self):
        self.adviser = ZigZagAdviser()

    def test_min_max(self):
        self.adviser.set_genome([1, 0.01, 0.01])
        self.adviser()
        data_i = self.adviser.data_i
        max_high = self.adviser.max_high
        max_high_i = self.adviser.max_high_i
        min_low = self.adviser.min_low
        min_low_i = self.adviser.min_low_i
        top_i = self.adviser.top_i
        bottom_i = self.adviser.bottom_i
        last_depth = self.adviser.last_depth

        # 最小値
        self.adviser.fetch_recent_data(price=0)
        self.assertEqual(data_i + 1, self.adviser.data_i)
        self.assertEqual(0, self.adviser.min_low)
        self.assertEqual(data_i + 1, self.adviser.min_low_i)
        # 最大値
        self.adviser.fetch_recent_data(price=10**5)
        self.assertEqual(data_i + 2, self.adviser.data_i)
        self.assertEqual(10**5, self.adviser.max_high)
        self.assertEqual(data_i + 2, self.adviser.max_high_i)

    def test_trend(self):
        self.adviser.set_genome([1, 0.01, 0.01])
        self.adviser()
        data_i = self.adviser.data_i
        max_high = self.adviser.max_high
        max_high_i = self.adviser.max_high_i
        min_low = self.adviser.min_low
        min_low_i = self.adviser.min_low_i
        top_i = self.adviser.top_i
        bottom_i = self.adviser.bottom_i
        last_depth = self.adviser.last_depth
        trend = self.adviser.trend
        # 値幅率を上に超える
        self.adviser.fetch_recent_data(price=10 ** 5)
        self.adviser.fetch_recent_data(price=10 ** 4)
        self.adviser.fetch_recent_data(price=10 ** 3)
        self.assertEqual(self.adviser.OTHER, self.adviser.trend)
        self.assertEqual(self.adviser.decision_term, 2)
        self.adviser.fetch_recent_data(price=10 ** 2)
        self.assertEqual(self.adviser.TOP, self.adviser.trend)

        self.assertEqual(self.adviser.max_high, 10 ** 5)
        self.assertEqual(self.adviser.max_high_i, data_i + 1)
        self.assertEqual(self.adviser.min_low, 10 ** 2)
        self.assertEqual(self.adviser.min_low_i, data_i + 4)

        # 値幅率を下に超える
        self.adviser.fetch_recent_data(price=1)
        self.adviser.fetch_recent_data(price=2)
        self.adviser.fetch_recent_data(price=3)
        self.assertEqual(self.adviser.OTHER, self.adviser.trend)
        self.assertEqual(self.adviser.decision_term, 2)
        self.adviser.fetch_recent_data(price=4)
        self.assertEqual(self.adviser.BOTTOM, self.adviser.trend)

        self.assertEqual(self.adviser.max_high, 4)
        self.assertEqual(self.adviser.max_high_i, data_i + 4 + 4)
        self.assertEqual(self.adviser.min_low, 1)
        self.assertEqual(self.adviser.min_low_i, data_i + 1 + 4)


if __name__ == '__main__':
    unittest.main()
