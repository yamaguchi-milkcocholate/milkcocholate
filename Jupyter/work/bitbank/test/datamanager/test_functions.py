import sys
import os
import unittest
import pandas as pd
sys.path.append(os.pardir + '/../')
from modules.datamanager import functions


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_moving_average(self):
        list_1 = [1, 1, 1, 4, 4, 10]
        df_1 = pd.DataFrame(data=list_1, columns=['end'])
        result_1 = functions.simple_moving_average(candlestick_end=df_1, term=3)
        # [1, 2, 3, 6]
        self.assertEqual(4, len(result_1))
        self.assertEqual(1, result_1.at[0, 'simple_moving_average'])
        self.assertEqual(2, result_1.at[1, 'simple_moving_average'])
        self.assertEqual(3, result_1.at[2, 'simple_moving_average'])
        self.assertEqual(6, result_1.at[3, 'simple_moving_average'])
        # 例外
        try:
            df_1 = pd.DataFrame(data=list_1, columns=['hoge'])
            functions.simple_moving_average(candlestick_end=df_1, term=3)
            self.assertEqual(1, -1, msg='カラム名の例外')
        except TypeError:
            pass

    def test_exponential_moving_average(self):
        list_1 = [1, 1, 4, 6, 16, 20]
        df_1 = pd.DataFrame(data=list_1, columns=['end'])
        result_1 = functions.exponential_moving_average(candlestick_end=df_1, term=3)
        # [2, 4, 10, 15]
        self.assertEqual(4, len(result_1))
        self.assertEqual(2, result_1.at[0, 'exponential_moving_average'])
        self.assertEqual(4, result_1.at[1, 'exponential_moving_average'])
        self.assertEqual(10, result_1.at[2, 'exponential_moving_average'])
        self.assertEqual(15, result_1.at[3, 'exponential_moving_average'])
        # 例外
        try:
            df_1 = pd.DataFrame(data=list_1, columns=['hoge'])
            functions.simple_moving_average(candlestick_end=df_1, term=3)
            self.assertEqual(1, -1, msg='カラム名の例外')
        except TypeError:
            pass

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
