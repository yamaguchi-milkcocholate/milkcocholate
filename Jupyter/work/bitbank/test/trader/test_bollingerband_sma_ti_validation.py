import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from modules.trader.bollingerband_sma_ti_validation import BollingerBandSMATiValidationTrader
from modules.datamanager.picker import Picker


class TestBollingerBandSMATiValidationTrader(unittest.TestCase):

    def setUp(self):
        self.__trader = BollingerBandSMATiValidationTrader(
            stock_term=20,
            inclination_alpha=9
        )
        candlestick = Picker(span='5min', use_of_data='validation', coin='xrp').get_candlestick()
        self.__trader.set_candlestick(candlestick=candlestick)
        self.__trader.set_genome(
            host='192.168.99.100',
            population_id='365',
            individual_num=0
        )
        self.__trader.fetch_has_coin(has_coin=True)

    def test_operation(self):
        self.__trader.operation()


if __name__ == '__main__':
    unittest.main()
