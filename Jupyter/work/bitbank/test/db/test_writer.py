import os
import sys
import unittest
sys.path.append(os.path.pardir + '/../')
from modules.db import writer


class TestWriter(unittest.TestCase):

    def setUp(self):
        self.writer = writer.Writer('localhost')

    def test_write(self):
        table = ''
        columns = []
        value = []
        #self.writer.write(table, columns, value)

    def test_rollback(self):
        self.writer.begin_transaction()
        table = 'genetic_algorithms'
        columns = ['id', 'name', 'spec']
        value = [1, 'test', 'test']
        self.writer.write(table, columns, value)
        self.writer.rollback()

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
