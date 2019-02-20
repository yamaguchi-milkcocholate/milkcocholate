import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from bitbank.adviser.tag import Tag


class TestTag(unittest.TestCase):

    def setUp(self):
        self.ema_term = 5
        self.ma_term = 9
        self.adviser = Tag(ema_term=5, ma_term=9, directory='../../15min/training/gp_03.pkl')

    def tearDown(self):
        pass

    def test_tag_candlestick(self):
        self.assertEqual(self.ma_term - 1, len(self.adviser.ma_list))
        self.assertEqual(self.ema_term - 1, len(self.adviser.ema_list))
        self.assertEqual(self.ma_term - 1, len(self.adviser.data))
        """
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
        """

    def test_regression(self):
        w, e = self.adviser.ma_regression()

    def test_guess(self):
        price = self.adviser.guess_price_ma(ma=32.373)

    def test_analysis(self):
        operation, price, order_type = self.adviser.analysis(
            inc=0,
            e=0,
            ema_price_diff=0,
            ema_ma_diff=0,
            ma_diff=0,
            board=0,
            has_coin=True,
            is_waiting=True,
            buying_price=0
        )
        print(operation)


if __name__ == '__main__':
    unittest.main()
