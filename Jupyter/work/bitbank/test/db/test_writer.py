import os
import sys
import unittest
sys.path.append(os.path.pardir + '/../')
from modules.db import writer


class TestWriter(unittest.TestCase):

    def setUp(self):
        self.writer = writer.Writer('localhost')

    def test_write_chunk_with_auto_increment_id(self):
        table = 'genetic_algorithms'
        columns = ['name', 'spec']
        value = [
            ['chunk1', 'chunk2'],
            ['chunk1', 'chunk2'],
        ]
        self.writer.write_chunk_with_auto_increment_id(table, columns, value)

    def test_write(self):
        table = 'genetic_algorithms'
        columns = ['name', 'spec']
        value = ['test', 'test']
        self.writer.write(table, columns, value)
        columns = ['id', 'name', 'spec']
        value = ['test', 'test']
        self.writer.write(table, columns, value)
        columns = ['name', 'spec']
        value = [1, 'test', 'test']
        self.writer.write(table, columns, value)
        columns = ['id', 'name', 'spec']
        value = [1000, 'test', 'test']
        self.writer.write(table, columns, value)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
