import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from modules.fitnessfunction.inclination_optimization import InclinationOptimization


class TestInclinationOptimization(unittest.TestCase):

    def setUp(self):
        self.__inclination_optimization = InclinationOptimization(
            sma_term=12,
            std_term=12,
            stock_term=12,
            inclination_alpha=2.5
        )

    def test_call(self):
        pass
        self.__inclination_optimization()

    def test_inclination_pattern(self):
        self.__inclination_optimization.inclination_pattern(1)
        check = self.__inclination_optimization.get_inclination_check()
        print(check)


if __name__ == '__main__':
    unittest.main()
