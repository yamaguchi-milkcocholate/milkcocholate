import sys
import os
import unittest
import pprint
sys.path.append(os.pardir+'/../')
from modules.datamanager import apigateway


class TestApiGateway(unittest.TestCase):

    def setUp(self):
        pair = 'btc_jpy'
        self.gateway = apigateway.ApiGateway(pair)

    def test_use_ticker(self):
        ticker = self.gateway.use_ticker()
        pprint.pprint(ticker)
        print(type(ticker))

    def test_use_depth(self):
        depth = self.gateway.use_depth()
        pprint.pprint(depth)
        print(type(depth))

    def test_use_candlestick(self):
        candlestick = self.gateway.use_candlestick('20181005', '1hour')
        pprint.pprint(candlestick)
        print(type(candlestick))


if __name__ == '__main__':
    unittest.main()
