import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from modules.datamanager.zigzag import ZigZag


class TestZigZag(unittest.TestCase):

    def setUp(self):
        self.zigzag = ZigZag()

    def test_init(self):
        result = self.zigzag.get_candlestick()
        print(result)


if __name__ == '__main__':
    unittest.main()
