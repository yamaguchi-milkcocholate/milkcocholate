import os
import sys
import unittest
import pprint
sys.path.append(os.pardir + '/../../')
from flask_modules.loggraph.repository import exptrepo


class TestExperimentRepository(unittest.TestCase):

    def setUp(self):
        self._repository = exptrepo.ExperimentRepository(host='localhost')

    def test_get_experiments(self):
        result = self._repository.get_experiments()
        for item in result:
            pprint.pprint(vars(item))


if __name__ == '__main__':
    unittest.main()
