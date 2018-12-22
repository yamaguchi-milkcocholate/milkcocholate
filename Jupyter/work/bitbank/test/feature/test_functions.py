import os
import sys
import unittest
import pprint
sys.path.append(os.path.pardir + '/../')
from modules.feature import functions


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def test_bollinger_band(self):
        situation = functions.bollinger_band()
        # pprint.pprint(situation.get_genome_ranges())

    def test_wave_template(self):
        waves = {'sma': 20, 'ema': 10}
        situation = functions.wave_template(waves=waves, pattern_num=3)
        pprint.pprint(situation.get_genome_ranges())

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
