import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from modules.trader.macd import MACDTrader


class TestMACDTrader(unittest.TestCase):

    def setUp(self):
        self.trader = MACDTrader(
            is_exist_pickle=True
        )

    def test_init(self):
        print(self.trader.data)
        pass

    def test_genome(self):
        self.trader.set_genome(
            host='localhost',
            population_id=420,
            individual_num=1
        )


if __name__ == '__main__':
    unittest.main()
