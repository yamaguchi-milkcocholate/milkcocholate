import unittest
import sys
import os
import numpy as np
sys.path.append(os.pardir+'/../')
from modules.crossover import cfacade


class TestSelectElites(unittest.TestCase):

    def setUp(self):
        crossover_facade = cfacade.CrossoverFacade()
        self._crossover = crossover_facade.select_department(crossover_name='one_point')

    def test_select_elites(self):
        """
        エリート個体を選択できているかチェック
        :return:
        """
        geno_type = np.asarray([[1, 10], [2, 20], [3, 30], [4, 40]])
        fitness = np.asarray([10, 20, 30, 40])
        elite_num = 2
        elites = self._crossover.select_elites(
            elite_num=elite_num,
            geno_type=geno_type,
            fitness=fitness
        )
        self.assertIsInstance(elites, type(np.asarray([])))
        self.assertIsInstance(elites[0], type(np.asarray([])))
        self.assertEqual(elites[0][0], 4)
        self.assertEqual(elites[0][1], 40)
        self.assertEqual(elites[1][0], 3)
        self.assertEqual(elites[1][1], 30)


if __name__ == '__main__':
    unittest.main()
