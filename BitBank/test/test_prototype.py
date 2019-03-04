"""
inc           : -0.02865
e             : 0.00160
ema price diff: 0.21690
ema ma diff   : -0.18076
ma diff       : -0.17633
"""
import os
import sys
import unittest
sys.path.append(os.pardir)
from bitbank.prototype import Prototype
from bitbank.adviser.tag import Tag


class TestPrototype(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testMain(self):
        adviser = Tag(ema_term=3, ma_term=6, buy_directory='../15min/training/aggregate_gp_02.pkl',
                      sell_directory='../15min/training/gp_next_03.pkl')

        bot = Prototype(
            adviser=adviser,
            pair='xrp_jpy',
            log='../15min/log/test_01.txt'
        )
        bot.request(operation=bot.BUY, price=100, order_type=adviser.TYPE_LIMIT)
        bot.request(operation=bot.SELL, price=100, order_type=adviser.TYPE_LIMIT)
        bot.request(operation=bot.RETRY, price=100, order_type=adviser.TYPE_LIMIT)


if __name__ == '__main__':
    unittest.main()
