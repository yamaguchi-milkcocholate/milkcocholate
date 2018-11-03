import os
import sys
import unittest
import pprint
sys.path.append(os.pardir + '/../../')
from flask_modules.loggraph.repository import loggraprepo


class TestLogGraphRepository(unittest.TestCase):

    def setUp(self):
        self._repository = loggraprepo.LogGraphRepository(host='localhost')

    def test_get_log_graph(self):
        result = self._repository.get_log_graph(population_id=1)
        pprint.pprint(result.plot_data)


if __name__ == '__main__':
    unittest.main()
