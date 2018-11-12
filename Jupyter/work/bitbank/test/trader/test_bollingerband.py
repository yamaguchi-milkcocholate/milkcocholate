import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from modules.trader.bollingerband import BollingerBandTrader


class TestBollingerBand(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
