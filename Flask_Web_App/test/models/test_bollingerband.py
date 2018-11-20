import os
import sys
import unittest
import pprint
sys.path.append(os.pardir + '/../')
from models.bollingerband import BollingerBand


class TestBollingerBand(unittest.TestCase):

    def setUp(self):
        self.__bollingerband = BollingerBand(host='localhost')

    def test_call(self):
        result = self.__bollingerband()
        genome = self.__bollingerband.get_genome()
        situation = self.__bollingerband.get_situation()
        test_dict = dict()
        index = 0
        for key in situation[0]:
            test_dict[key] = genome[0][index]
            index += 1
        # stayの時を取り出してみる
        for pattern in test_dict:
            if test_dict[pattern] == 3:
                print(pattern, test_dict[pattern])


if __name__ == '__main__':
    unittest.main()
