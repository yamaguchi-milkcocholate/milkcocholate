import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from models.bollingerband_ti import BollingerBandTi


class TestBollingerBandTi(unittest.TestCase):

    def setUp(self):
        self.__bolligerband_ti = BollingerBandTi(host='localhost')

    def test_call(self):
        result = self.__bolligerband_ti()
        genome = self.__bolligerband_ti.get_genome()
        situation = self.__bolligerband_ti.get_situation()
        print(result)


if __name__ == '__main__':
    unittest.main()
