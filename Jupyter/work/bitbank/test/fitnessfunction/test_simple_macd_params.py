import unittest
import sys
import os
import numpy as np
sys.path.append(os.pardir+'/../')
from modules.fitnessfunction import fffacade
from modules.db import facade


class TestSimpleMacdParams(unittest.TestCase):

    def setUp(self):
        ff_facade = fffacade.Facade(candle_type='1hour')
        db_facade = facade.Facade(host='localhost')
        db_dept = db_facade.select_department(table='experiment_logs')
        self._fitness_function = ff_facade.select_department(
            function_name='simple_macd_params',
            db_dept=db_dept
        )
        self._geno_type = np.asarray([
            [10, 20, 10],
            [11, 22, 11],
        ])
        self._approach = self._fitness_function.get_approach()

    def test_calc_fitness(self):
        pass

    def test_calc_result(self):
        data = self._approach(
            self._geno_type[0][0],
            self._geno_type[0][1],
            self._geno_type[0][2],
        )
        #self._fitness_function.calc_result(data=data)

    def test_calc_result_and_log(self):
        data = self._approach(
            self._geno_type[0][0],
            self._geno_type[0][1],
            self._geno_type[0][2],
        )
        #self._fitness_function.calc_result_and_log(data=data, population_id=2000)


if __name__ == '__main__':
    unittest.main()
