import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from modules.gn.condition import Condition


class TestCondition(unittest.TestCase):

    def setUp(self):
        self.condition = Condition()

    def test_add_technical_analysis(self):
        self.condition.add_technical_analysis(
            name='bolingerband',
            lower_limit=0.1,
            upper_limit=10
        )
        print(self.condition.technical_analysis)


if __name__ == '__main__':
    unittest.main()
