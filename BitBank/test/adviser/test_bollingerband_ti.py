import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from bitbank.adviser.bollingerband_ti import BollingerBandTiAdviser


class TestBollingerBandTiAdviser(unittest.TestCase):

    def setUp(self):
        self.__adviser = BollingerBandTiAdviser(
            stock_term=12,
            inclination_alpha=2,
            pair='xrp_jpy'
        )

    def test_fetch_recent_data(self):
        print(self.__adviser.get_recent_data())
        self.__adviser.fetch_recent_data()
        print(self.__adviser.get_recent_data())


if __name__ == '__main__':
    unittest.main()
