import sys
import os
import unittest
sys.path.append(os.pardir)
from bitbank.bot import Bot
from bitbank.adviser.bollingerband_ti import BollingerBandTiAdviser


class TestBot(unittest.TestCase):

    def setUp(self):
        print('api key = ', end='')
        api_key = input()
        print('api secret = ', end='')
        api_secret = input()
        adviser = BollingerBandTiAdviser(
            stock_term=20,
            inclination_alpha=400,
            pair='xrp_jpy'
        )
        self.__bot = Bot(
            host='localhost',
            population_id=271,
            genome_id=0,
            adviser=adviser,
            pair='xrp_jpy',
            api_key=api_key,
            api_secret=api_secret
        )

    def test_init(self):
        genome = self.__bot.genome
        self.assertEqual(360, len(genome))


if __name__ == '__main__':
    unittest.main()
