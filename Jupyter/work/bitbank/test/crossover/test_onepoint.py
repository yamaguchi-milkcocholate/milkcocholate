import unittest
import sys
import os
import numpy as np
sys.path.append(os.pardir+'/../')
from modules.crossover import cfacade
from modules.feature import genofeature


class TestOnePointCrossover(unittest.TestCase):

    def setUp(self):
        crossover_facade = cfacade.CrossoverFacade()
        self._crossover = crossover_facade.select_department(crossover_name='one_point')
        self._mutation = 50
        self._cross = 50
        self._elite_num = 1
        self._population = 4
        self._situation = genofeature.Situation()
        self._situation.set_fitness_function_id(1000)
        self._situation.set_genome_ranges(
            param_1=(1, 50),
            param_2=(50, 100),
        )
        self._geno_type = np.asarray([[1, 10], [2, 20], [3, 30], [4, 40]])
        self._fitness = np.asarray([10, 20, 30, 40])

    def test_determine_next_generation(self):
        """
        遺伝子の次元が変わっていないかチェックする
        """

        geno_type = self._crossover.determine_next_generation(
            geno_type=self._geno_type,
            fitness=self._fitness,
            situation=self._situation,
            mutation=self._mutation,
            cross=self._cross,
            elite_num=self._elite_num,
        )
        self.assertIsInstance(geno_type, type(np.asarray([])))
        self.assertIsInstance(geno_type[0], type(np.asarray([])))
        self.assertIsInstance(geno_type[0][0], type(np.asarray([1])[0]))
        self.assertEqual(len(geno_type), self._population)


if __name__ == '__main__':
    unittest.main()
