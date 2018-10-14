# coding:utf-8
import unittest
import sys
import os
sys.path.append(os.pardir)
from modules.ga import sga


class TestQuadraticEquation(unittest.TestCase):
    """
    unittestのテスト
    """
    def setUp(self):
        print("setup")
        situation = list()
        situation.append((1, 50))
        self.ga = sga.SimpleGeneticAlgorithm(situation, None)

    def test_calc_root(self):
        """
        SUCCESS
        """
        expected = (-1.0, -1.0)
        self.assertEquals(expected[0], expected[1])

    def test_calc_value(self):
        """
        FAIL
        """
        expected = (4.0, 9.0)
        self.assertEquals(expected[0], expected[1])

    def tearDown(self):
        print("tearDown")
        del self.ga


if __name__ == '__main__':
    unittest.main()
