import sys
import os
import unittest
import numpy as np
from pprint import pprint
sys.path.append(os.pardir)
from bitbank.apigateway import ApiGateway


class TestApiGateway(unittest.TestCase):

    def setUp(self):
        print('api_key: ', end="")
        api_key = ''
        print('api_secret: ', end="")
        api_secret = ''
        self.api_gateway = ApiGateway(api_key=api_key, api_secret=api_secret)
        self.order_id = None

    def test_use_depth(self):
        result = self.api_gateway.use_depth(pair='xrp_jpy')
        self.assertNotEqual(None, result['asks'])
        self.assertNotEqual(None, result['bids'])

    def test_use_ticker(self):
        result = self.api_gateway.use_ticker(pair='xrp_jpy')
        self.assertNotEqual(None, result['sell'])
        self.assertNotEqual(None, result['buy'])
        self.assertNotEqual(None, result['high'])
        self.assertNotEqual(None, result['low'])
        self.assertNotEqual(None, result['last'])
        self.assertNotEqual(None, result['vol'])
        result = self.api_gateway.use_ticker(pair='xrp_jpy')
        self.assertNotEqual(None, result['sell'])
        self.assertNotEqual(None, result['buy'])
        self.assertNotEqual(None, result['high'])
        self.assertNotEqual(None, result['low'])
        self.assertNotEqual(None, result['last'])
        self.assertNotEqual(None, result['vol'])

    def test_use_candlestick(self):
        result = self.api_gateway.use_candlestick(pair='xrp_jpy', candle_type='5min', time='20181130')
        self.assertNotEqual(None, result['candlestick'])
        self.assertEqual('5min', result['candlestick'][0]['type'])
        self.assertEqual(12 * 24, len(result['candlestick'][0]['ohlcv']))

    def test_order(self):
        # new_order
        print('price: ', end='')
        self.price = input()
        print('amount: ', end='')
        self.amount = input()
        print('side: ', end='')
        self.side = input()
        result = self.api_gateway.new_order(
            pair='xrp_jpy',
            price=self.price,
            amount=self.amount,
            side=self.side,
            order_type='limit'
        )
        self.assertNotEqual(None, result['order_id'])
        self.assertEqual('xrp_jpy', result['pair'])
        self.assertEqual(self.side, result['side'])
        self.assertEqual('limit', result['type'])
        self.assertEqual(self.amount, int(result['start_amount']))
        self.assertNotEqual(None, result['executed_amount'])
        self.assertEqual(self.price, result['price'])
        self.assertNotEqual(None, result['average_price'])
        self.assertNotEqual(None, result['ordered_at'])
        self.assertNotEqual(None, result['status'])
        self.order_id = result['order_id']
        print(result)

        # cancel_order
        result = self.api_gateway.cancel_order(
            pair='xrp_jpy',
            order_id=self.order_id
        )
        self.assertEqual(self.order_id, result['order_id'])
        self.assertEqual('xrp_jpy', result['pair'])
        self.assertEqual(self.side, result['side'])
        self.assertEqual('limit', result['type'])
        self.assertEqual(self.amount, int(result['start_amount']))
        self.assertNotEqual(None, result['executed_amount'])
        self.assertEqual(self.price, result['price'])
        self.assertNotEqual(None, result['average_price'])
        self.assertNotEqual(None, result['ordered_at'])
        self.assertNotEqual(None, result['status'])
        print(result)

        # order_info
        result = self.api_gateway.use_orders_info(
            pair='xrp_jpy',
            order_ids=[self.order_id]
        )
        self.assertEqual(self.order_id, result['orders'][0]['order_id'])
        self.assertEqual('xrp_jpy', result['orders'][0]['pair'])
        self.assertEqual(self.side, result['orders'][0]['side'])
        self.assertEqual('limit', result['orders'][0]['type'])
        self.assertEqual(self.amount, int(result['orders'][0]['start_amount']))
        self.assertNotEqual(None, result['orders'][0]['executed_amount'])
        self.assertEqual(self.price, result['orders'][0]['price'])
        self.assertNotEqual(None, result['orders'][0]['average_price'])
        self.assertNotEqual(None, result['orders'][0]['ordered_at'])
        self.assertNotEqual(None, result['orders'][0]['status'])
        print(result)


if __name__ == '__main__':
    unittest.main()
