import os
import sys
import unittest
sys.path.append(os.pardir + '/../')
from flask_modules.db import reader


class TestReader(unittest.TestCase):

    def setUp(self):
        self._reader = reader.Reader('localhost')

    def test_execute_query(self):
        sql = "SELECT * FROM `experiment_logs` WHERE `id` = %s;"
        placeholder = [5]
        result = self._reader.execute_query(sql=sql, placeholder=placeholder)
        self.assertEqual(5, result['id'])
        self.assertEqual(1, result['population_id'])
        self.assertEqual(1023882, result['position'])
        self.assertEqual(935140, result['price'])
        self.assertEqual('2018-02-12 14:00:00', result['logged_at'].strftime('%Y-%m-%d %H:%M:%S'))

    def test_method_chain(self):
        self._reader('experiment_logs').select().where(['id', '=', 5])
        result = self._reader.get(should_execute=True)
        self.assertEqual(5, result['id'])
        self.assertEqual(1, result['population_id'])
        self.assertEqual(1023882, result['position'])
        self.assertEqual(935140, result['price'])
        self.assertEqual('2018-02-12 14:00:00', result['logged_at'].strftime('%Y-%m-%d %H:%M:%S'))


if __name__ == '__main__':
    unittest.main()
