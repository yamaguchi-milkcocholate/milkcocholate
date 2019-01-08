import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from bitbank.adviser.zigzag import ZigZagAdviser


class TestZigZag(unittest.TestCase):

    def setUp(self):
        self.adviser = ZigZagAdviser()

    def test_main(self):
        self.adviser.set_genome([1, 0.01])
        self.adviser()
        self.adviser.fetch_recent_data()
        print(
            self.adviser.max_high,
            self.adviser.min_low,
            self.adviser.max_high_i,
            self.adviser.min_low_i,
            self.adviser.top_i,
            self.adviser.bottom_i,
            self.adviser.last_depth,
            self.adviser.data_i,
            self.adviser.price,
            self.adviser.trend,
        )


if __name__ == '__main__':
    unittest.main()
