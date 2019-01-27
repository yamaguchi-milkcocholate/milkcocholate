import sys
import os
import unittest
import numpy as np
sys.path.append(os.pardir)
from bitbank.functions import *


class TestFunctions(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_cosine_similarity(self):
        x = np.asarray([1, 0, 1, 0])
        y = np.asarray([1, 0, 1, 0])
        sim = cosine_similarity(x, y)
        self.assertAlmostEqual(sim, 1)

        x = np.asarray([1, 0, 1, 0])
        y = np.asarray([0, 1, 0, 1])
        sim = cosine_similarity(x, y)
        self.assertAlmostEqual(sim, 0)

    def test_line(self):
        y = line(21, 1, 0)
        print(np.round(y, 2))
        self.assertEqual(21, len(y))


if __name__ == '__main__':
    unittest.main()
