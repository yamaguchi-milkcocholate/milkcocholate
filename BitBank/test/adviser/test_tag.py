import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from bitbank.adviser.tag import Tag


class TestTag(unittest.TestCase):

    def setUp(self):
        self.ema_term = 5
        self.ma_term = 9
        self.adviser = Tag(ema_term=5, ma_term=9)

    def tearDown(self):
        pass

    def test_tag_candlestick(self):
        self.assertEqual(self.ma_term - 1, len(self.adviser.ma_list))
        self.assertEqual(self.ema_term - 1, len(self.adviser.ema_list))
        self.assertEqual(self.ma_term - 1, len(self.adviser.data))

        self.adviser.fetch_recent_data(price=10000)

        self.adviser.update_data()
        self.assertEqual(10000, self.adviser.data[-1])
        self.assertEqual(self.ma_term - 1, len(self.adviser.data))

        self.adviser.update_ma()
        self.assertGreater(self.adviser.ma, 200)
        self.adviser.update_ema()
        self.assertGreater(self.adviser.ema, 200)

        self.adviser.update_ma_list()
        self.assertEqual(self.adviser.ma_list[-1], self.adviser.ma)
        self.adviser.update_ema_list()
        self.assertEqual(self.adviser.ema_list[-1], self.adviser.ema)

    def test_regression(self):
        w, e = self.adviser.ma_regression()

    def test_guess(self):
        price = self.adviser.guess_price_ma(ma=32.373)
        print(price)


if __name__ == '__main__':
    unittest.main()
