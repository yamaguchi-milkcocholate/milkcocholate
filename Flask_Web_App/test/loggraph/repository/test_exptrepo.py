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

    def test_get_experiment(self):
        result = self._repository.get_experiment(experiment_id=12)

    def test_get_bollingerband_ti(self):
        result = self._repository.get_bollingerband_ti()
        print(len(result))


if __name__ == '__main__':
    unittest.main()
