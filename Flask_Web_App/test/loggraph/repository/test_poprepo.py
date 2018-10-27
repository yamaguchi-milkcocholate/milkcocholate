import os
import sys
import unittest
import pprint
sys.path.append(os.pardir + '/../../')
from flask_modules.loggraph.repository import poprepo


class TestPopulationRepository(unittest.TestCase):

    def setUp(self):
        self._repository = poprepo.PopulationRepository('localhost')

    def test_get_population(self):
        result = self._repository.get_populations(experiment_id=1)
        for item in result:
            pprint.pprint(vars(item))


if __name__ == '__main__':
    unittest.main()
