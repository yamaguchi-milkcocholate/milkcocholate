import unittest
import sys
import os
import numpy as np
sys.path.append(os.pardir)
from modules.ga import ga


class TestGa(unittest.TestCase):

    def setUp(self):
        pass

    def test__init__(self):
        situation = list()
        situation.append((1, 10))
        elite_num = 1
        population = 101
        try:
            temp_ga = ga.GeneticAlgorithm(2, 70, [1, 5], population, elite_num)
            self.assertEquals(1, -1)
        except TypeError:
            pass
        try:
            temp_ga = ga.GeneticAlgorithm(2, 70, situation, population=population, elite_num=200)
            self.assertEquals(1, -1)
        except ArithmeticError:
            pass
        try:
            temp_ga = ga.GeneticAlgorithm(2, 70, situation, population=20, elite_num=elite_num)
            self.assertEquals(1, -1)
        except ArithmeticError:
            pass
        try:
            temp_ga = ga.GeneticAlgorithm(2, 70, situation, population=population, elite_num=elite_num)
        except TypeError as e:
            print(e)
            self.assertEquals(1, -1)
        except ArithmeticError as e:
            print(e)
            self.assertEquals(1, -1)
        del temp_ga

    def test_init_population(self):
        self.ga = ga.GeneticAlgorithm(2, 70, situation=[(1, 50)], population=10, elite_num=2)
        result = self.ga.init_population()
        self.assertIsInstance(result, type(np.asarray([1])))
        for i in result:
            self.assertLessEqual(i[0], 50)
            self.assertLessEqual(1, i[0])
            self.assertIsInstance(i, type(np.asarray([])))
        self.assertEqual(10, len(result))
        del self.ga

    def generation(self):
        self.ga = ga.GeneticAlgorithm(2, 70, situation=[(1, 50)], population=10, elite_num=2)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
