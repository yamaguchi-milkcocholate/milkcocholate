# coding:utf-8
import unittest
import sys
import os
import numpy as np
sys.path.append(os.pardir+'/../')
from modules.ga import sga
from modules.feature import genofeature


class TestSga(unittest.TestCase):
    def setUp(self):
        pass

    def test_determine_next_generation(self):
        """
        遺伝子の次元が変わっていないかチェックする
        """
        situation = genofeature.Situation()
        situation.set_fitness_function_id(1)
        situation.set_genome_ranges(
            param_1=(1, 50),
            param_2=(1, 50)
        )
        fitness_function = SampleFitnessFunction()
        self.ga = sga.SimpleGeneticAlgorithm(fitness_function=fitness_function, mutation=2, cross=70,
                                             situation=situation, population=4, elite_num=2)
        geno_type = np.asarray([[1, 10], [2, 20], [3, 30], [4, 40]])
        fitness = np.asarray([10, 20, 30, 40])
        geno_type = self.ga.determine_next_generation(geno_type, fitness)
        self.assertIsInstance(geno_type, type(np.asarray([])))
        self.assertIsInstance(geno_type[0], type(np.asarray([])))
        self.assertIsInstance(geno_type[0][0], type(np.asarray([1])[0]))
        self.assertEqual(len(geno_type), 4)
        del self.ga

    def tearDown(self):
        pass


class SampleFitnessFunction:
    """
    テスト用の適応度関数
    """
    
    def __init__(self):
        pass

    @staticmethod
    def calc_fitness(geno_type):
        return geno_type


if __name__ == '__main__':
    unittest.main()
