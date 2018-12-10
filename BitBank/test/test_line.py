import sys
import os
import unittest
sys.path.append(os.pardir)
from bitbank.line import Line


class TestLine(unittest.TestCase):

    def setUp(self):
        self.__line = Line()

    def test_call(self):
        self.__line.__call__(message='Hello World!')


if __name__ == '__main__':
    unittest.main()
