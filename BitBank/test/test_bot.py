import sys
import os
import unittest
sys.path.append(os.pardir)
from bitbank.bot import Bot


class TestBot(unittest.TestCase):

    def setUp(self):
        self.__bot = Bot(host='localhost', population_id=130, genome_id=0)

    def test_init(self):
        genome = self.__bot.genome
        self.assertEqual(180, len(genome))


if __name__ == '__main__':
    unittest.main()
