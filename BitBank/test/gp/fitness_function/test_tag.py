import sys
import os
import unittest
sys.path.append(os.pardir + '/../../')
from bitbank.gp.fitnessfunction.tag import TagFitnessFunction
from bitbank.gp.gpgenome import GPGenome


class TestTagFitnessFunction(unittest.TestCase):

    def setUp(self):
        self.tag = TagFitnessFunction(ema_term=4, ma_term=8, goal=0.1)

    def tearDown(self):
        pass

    def test_make_data_frame(self):
        data = self.tag.get_data()

    def test_calc_fitness(self):
        condition = self.tag.get_condition()
        genome = GPGenome(condition=condition)
        fitness = self.tag.calc_fitness(genomes=[genome])
        print(fitness)


if __name__ == '__main__':
    unittest.main()
