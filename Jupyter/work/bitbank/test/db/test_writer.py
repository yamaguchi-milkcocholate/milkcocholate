import os
import sys
import unittest
import pickle
import datetime
sys.path.append(os.path.pardir + '/../')
from modules.db import writer
from modules.feature import genofeature


class TestWriter(unittest.TestCase):

    def setUp(self):
        self.writer = writer.Writer('localhost')

    def test_write_with_auto_increment_id(self):
        self.writer.connect()
        table = 'test'
        columns = ['name', 'object', 'time']
        now = datetime.datetime.now()
        str_format = '%Y-%m-%d %H:%M:%S'
        situation_test = genofeature.Situation()
        situation_test.set_fitness_function_id(1000)
        situation_test.set_genome_ranges(
            short_term=(1, 50),
            long_term=(50, 100),
            signal=(1, 50)
        )
        value = [
            ['test_1', pickle.dumps(situation_test), now.strftime(str_format)],
            ['test_2', pickle.dumps(situation_test), now.strftime(str_format)],
        ]
        self.writer.write_with_auto_increment_id(table, columns, value)

    def test_next_auto_increment_id(self):
        self.writer.connect()
        auto_increment_id = self.writer.next_auto_increment_id('test')
        print(auto_increment_id)


if __name__ == '__main__':
    unittest.main()
