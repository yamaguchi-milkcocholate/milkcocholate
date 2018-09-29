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

    def test_calc_fitness(self):
        fitness_function = SampleFitnessFunction()
        self.ga = ga.GeneticAlgorithm(2, 70, situation=[(1, 50)], population=10, elite_num=2)
        geno_type = np.asarray([[1, 2], [3, 4], [5, 6]])
        fitness = self.ga.calc_fitness(geno_type, fitness_function)
        self.assertEqual(fitness[0][0], 1)
        self.assertEqual(fitness[0][1], 2)
        self.assertEqual(fitness[1][0], 3)
        self.assertEqual(fitness[1][1], 4)
        self.assertEqual(fitness[2][0], 5)
        self.assertEqual(fitness[2][1], 6)
        del self.ga

    def test_select_elites(self):
        self.ga = ga.GeneticAlgorithm(2, 70, situation=[(1, 50), (1, 50)], population=4, elite_num=2)
        geno_type = np.asarray([[1, 10], [2, 20], [3, 30], [4, 40]])
        fitness = np.asarray([10, 20, 30, 40])
        elites = self.ga.select_elites(geno_type, fitness)
        self.assertIsInstance(elites, type(np.asarray([])))
        self.assertIsInstance(elites[0], type(np.asarray([])))
        self.assertEqual(elites[0][0], 4)
        self.assertEqual(elites[0][1], 40)
        self.assertEqual(elites[1][0], 3)
        self.assertEqual(elites[1][1], 30)

        def tearDown(self):
            pass


class SampleFitnessFunction:

    @staticmethod
    def calc_fitness(geno_type):
        return geno_type


if __name__ == '__main__':
    unittest.main()
