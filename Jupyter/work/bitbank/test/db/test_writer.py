import os
import sys
import unittest
sys.path.append(os.path.pardir + '/../')
from modules.db import writer


class TestWriter(unittest.TestCase):

    def setUp(self):
        self.writer = writer.Writer('localhost')

    def test_write_with_auto_increment_id(self):
        table = 'genetic_algorithms'
        columns = ['name', 'spec']
        value = [
            ['chunk1', 'chunk2'],
            ['chunk1', 'chunk2'],
        ]
        self.writer.write_chunk_with_auto_increment_id(table, columns, value)


if __name__ == '__main__':
    unittest.main()
