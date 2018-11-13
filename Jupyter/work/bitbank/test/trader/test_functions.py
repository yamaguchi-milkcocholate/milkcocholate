import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from modules.trader import functions


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_simple_moving_average(self):
        input_list = [1, 1, 1, 4, 4, 10]
        result = functions.simple_moving_average(data=input_list, term=3)
        # [1, 2, 3, 6]
        self.assertEqual(4, len(result))
        self.assertEqual(1, result[0])
        self.assertEqual(2, result[1])
        self.assertEqual(3, result[2])
        self.assertEqual(6, result[3])

    def test_standard_deviation(self):
        input_list = [1, 2, 2, 4, 5, 6]
        result = functions.standard_deviation(data=input_list, term=3)
        # 標準偏差
        std_std = [0.471405, 0.942809, 1.247219, 0.816497]
        self.assertEqual(4, len(result))
        self.assertAlmostEqual(std_std[0], result[0], -5)
        self.assertAlmostEqual(std_std[1], result[1], -5)
        self.assertAlmostEqual(std_std[2], result[2], -5)
        self.assertAlmostEqual(std_std[3], result[3], -5)

    def test_volatility(self):
        # 単純移動平均線
        input_list = 10
        # 標準偏差
        std_std = 0.471405
        result = functions.volatility(sma=input_list, std=std_std)
        print(result)


if __name__ == '__main__':
    unittest.main()
