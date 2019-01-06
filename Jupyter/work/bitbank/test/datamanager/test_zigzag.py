import os
import sys
import unittest
import pandas as pd
sys.path.append(os.pardir + '/../')
from modules.datamanager.zigzag import ZigZag


class TestZigZag(unittest.TestCase):

    def setUp(self):
        self.zigzag = ZigZag()


if __name__ == '__main__':
    unittest.main()
