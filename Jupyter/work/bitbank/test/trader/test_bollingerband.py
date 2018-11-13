import sys
import os
import unittest
import datetime
sys.path.append(os.pardir + '/../')
from modules.trader.bollingerband import BollingerBandTrader
from modules.datamanager.apigateway import ApiGateway


class TestBollingerBand(unittest.TestCase):
    """
    注意：5minに設定しているため、5の倍数分で実行するとエラーになることがあります。
    """

    def setUp(self):
        self.__api_gateway = ApiGateway(pair='btc_jpy')
        self.__today = datetime.datetime.today().strftime('%Y%m%d')

    def test_dispose_candlestick(self):
        # listであればなんでも良い
        candlestick = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        candlestick_test = BollingerBandTrader.dispose_candlestick(
            stock_term=3,
            candlestick=candlestick
        )
        self.assertEqual(4, candlestick_test[0])
        self.assertEqual(5, candlestick_test[1])
        self.assertEqual(6, candlestick_test[2])
        self.assertEqual(7, candlestick_test[3])
        self.assertEqual(8, candlestick_test[4])
        self.assertEqual(9, candlestick_test[5])
        self.assertEqual(10, candlestick_test[6])
        # 例外のチェック
        try:
            candlestick = [1, 2, 3]
            BollingerBandTrader.dispose_candlestick(
                stock_term=3,
                candlestick=candlestick
            )
            self.assertEqual(1, -1)
        except TypeError:
            pass

    def test_operation(self):
        # まずは__init__のテスト
        trader = BollingerBandTrader(
            stock_term=3,
            inclination_alpha=2000,
            candle_type='5min'
        )
        # 計算の元になる終値は全てをチェック
        recent_data = trader.get_recent_data()
        candlestick = self.__api_gateway.use_candlestick(
            time=self.__today,
            candle_type='5min'
        )['candlestick'][0]['ohlcv']
        candlestick_size = len(candlestick)
        self.assertEqual(3 * 3 - 2, len(recent_data))
        self.assertEqual(int(candlestick[candlestick_size - 7][3]), recent_data[0])
        self.assertEqual(int(candlestick[candlestick_size - 6][3]), recent_data[1])
        self.assertEqual(int(candlestick[candlestick_size - 5][3]), recent_data[2])
        self.assertEqual(int(candlestick[candlestick_size - 4][3]), recent_data[3])
        self.assertEqual(int(candlestick[candlestick_size - 3][3]), recent_data[4])
        self.assertEqual(int(candlestick[candlestick_size - 2][3]), recent_data[5])
        self.assertEqual(int(candlestick[candlestick_size - 1][3]), recent_data[6])
        # 終値以外のデータは終値を元に作っているのでデータ数のみをチェック
        recent_sma = trader.get_recent_sma()
        recent_sigma = trader.get_recent_sigma()
        recent_volatility = trader.get_volatility()
        self.assertEqual(3 * 2 - 1, len(recent_sma))
        self.assertEqual(3, len(recent_sigma))
        # sma, upper, double_upper, lower, double_lower
        self.assertEqual(5, len(recent_volatility))

        # ここからoperation()のテスト
        trader.set_genome(host='localhost', population_id=1)
        trader.operation()
        recent_data = trader.get_recent_data()
        # recent_data[0]は最新のデータに更新された
        self.assertEqual(int(candlestick[candlestick_size - 6][3]), recent_data[1])
        self.assertEqual(int(candlestick[candlestick_size - 5][3]), recent_data[2])
        self.assertEqual(int(candlestick[candlestick_size - 4][3]), recent_data[3])
        self.assertEqual(int(candlestick[candlestick_size - 3][3]), recent_data[4])
        self.assertEqual(int(candlestick[candlestick_size - 2][3]), recent_data[5])
        self.assertEqual(int(candlestick[candlestick_size - 1][3]), recent_data[6])
        recent_sma = trader.get_recent_sma()
        recent_sigma = trader.get_recent_sigma()
        recent_volatility = trader.get_volatility()
        self.assertEqual(3 * 2 - 1, len(recent_sma))
        self.assertEqual(3, len(recent_sigma))
        # sma, upper, double_upper, lower, double_lower
        self.assertEqual(5, len(recent_volatility))

    def test_set_genome(self):
        trader = BollingerBandTrader(
            stock_term=3,
            inclination_alpha=2000,
            candle_type='5min'
        )
        trader.set_genome(host='localhost', population_id=1)
        genome = trader.get_genome()
        self.assertEqual(180, len(genome))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
