# coding:utf-8
import unittest
import sys
import os
import numpy as np
sys.path.append(os.pardir+'/../')
from modules.ga import ga
from modules.feature import genofeature


class TestGa(unittest.TestCase):

    def setUp(self):
        pass

    def test__init__(self):
        """
        1. 遺伝子の取り得る範囲(situation)のチェック
        2. 世代数とエリート数のチェック
        :return:
        """
        situation = genofeature.Situation()
        situation.set_fitness_function_id(1000)
        situation.set_genome_ranges(
            param_1=(1, 50),
            param_2=(50, 100),
            param_3=(1, 20),
        )
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
        """
        遺伝子初期化時に次元が適当かどうかのチェック
        :return:
        """
        situation = genofeature.Situation()
        situation.set_fitness_function_id(1000)
        situation.set_genome_ranges(
            param_1=(1, 50),
        )
        self.ga = ga.GeneticAlgorithm(2, 70, situation=situation, population=10, elite_num=2)
        result = self.ga.init_population()
        self.assertIsInstance(result, type(np.asarray([1])))
        for i in result:
            self.assertLessEqual(i[0], 50)
            self.assertLessEqual(1, i[0])
            self.assertIsInstance(i, type(np.asarray([])))
        self.assertEqual(10, len(result))
        del self.ga

    def test_calc_fitness(self):
        """
        適応度の次元が適当かどうかのチェック
        :return:
        """
        situation = genofeature.Situation()
        situation.set_fitness_function_id(1000)
        situation.set_genome_ranges(
            param_1=(1, 50),
        )
        fitness_function = SampleFitnessFunction()
        self.ga = ga.GeneticAlgorithm(2, 70, situation=situation, population=10, elite_num=2)
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
        """
        エリート個体を選択できているかチェック
        :return:
        """
        situation = genofeature.Situation()
        situation.set_fitness_function_id(1000)
        situation.set_genome_ranges(
            param_1=(1, 50),
            param_2=(1, 50),
        )
        self.ga = ga.GeneticAlgorithm(2, 70, situation=situation, population=4, elite_num=2)
        geno_type = np.asarray([[1, 10], [2, 20], [3, 30], [4, 40]])
        fitness = np.asarray([10, 20, 30, 40])
        elites = self.ga.select_elites(geno_type, fitness)
        self.assertIsInstance(elites, type(np.asarray([])))
        self.assertIsInstance(elites[0], type(np.asarray([])))
        self.assertEqual(elites[0][0], 4)
        self.assertEqual(elites[0][1], 40)
        self.assertEqual(elites[1][0], 3)
        self.assertEqual(elites[1][1], 30)


class SampleFitnessFunction:
    """
    テスト用の適応度関数
    """

    @staticmethod
    def calc_fitness(geno_type):
        return geno_type


if __name__ == '__main__':
    unittest.main()
