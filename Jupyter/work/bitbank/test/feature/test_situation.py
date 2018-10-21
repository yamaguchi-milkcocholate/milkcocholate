import os
import sys
import unittest
sys.path.append(os.path.pardir + '/../')
from modules.feature import genofeature


class TestSituation(unittest.TestCase):

    def setUp(self):
        self.situation = genofeature.Situation()
        self.situation.set_fitness_function_id(1000)
        self.situation.set_genome_ranges(
            short_term=(1, 50),
            long_term=(50, 100),
            signal=(1, 50)
        )

    def test_situation(self):
        fitness_function_id = self.situation.get_fitness_function()
        genomes = self.situation.get_genomes()
        genome_ranges = self.situation.get_genome_ranges()
        geno_tuple_list = self.situation.range_to_tuple_list()
        self.assertEqual(1000, fitness_function_id)
        self.assertListEqual(
            ['short_term', 'long_term', 'signal'],
            genomes
        )
        self.assertDictEqual(
            {
                'short_term': (1, 50),
                'long_term': (50, 100),
                'signal': (1, 50)
            },
            genome_ranges
        )
        self.assertListEqual(
            [
                (1, 50),
                (50, 100),
                (1, 50)
            ],
            geno_tuple_list
        )


if __name__ == '__main__':
    unittest.main()