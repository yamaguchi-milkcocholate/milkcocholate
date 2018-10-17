import unittest
import numpy as np
import os
import sys
sys.path.append(os.pardir + '/../')
from modules.ga import ga
from modules.feature import genofeature
from modules.fitnessfunction import fitnessfunction
from modules.crossover import crossover
from modules.db import facade


class TestGa(unittest.TestCase):

    def setUp(self):
        self._mutation = 50
        self._cross = 50
        self._elite_num = 1
        self._population = 101
        self._situation = genofeature.Situation()
        self._situation.set_fitness_function_id(1000)
        self._situation.set_genome_ranges(
            param_1=(1, 50),
            param_2=(50, 100),
            param_3=(1, 20),
        )
        self._db_facade = facade.Facade(host='localhost')
        expt_logs_dept = self._db_facade.select_department('experiment_logs')
        # 適応度関数
        self._fitness_function = SampleFitnessFunction(
            candle_type='5min',
            db_dept=expt_logs_dept,
            fitness_function_id=0
        )
        # 交叉手法
        self._crossover_method = SampleCrossover(crossover_id=0)

    def test__init__(self):
        """
        1. mutation(突然変異のパーセンテージ)は0 ~ 100
        2. cross(交叉のパーセンテージ)は0 ~ 100
        3. situation(遺伝子の特徴量を表す)はmodules.feature.Situationクラスのインスタンス
        4. population(個体数)がelite_num(エリートの個体数)より大きい
        5. crossover_method(交叉の手法を表す)はmodules.crossover.Crossoverクラスのインスタンス
        6. fitness_function(適応度関数を表す)はmodules.fitnessfunction.FitnessFunctionクラスのインスタンス
        """

        try:
            # mutation(突然変異のパーセンテージ)は0 ~ 100
            test_ga = ga.GeneticAlgorithm(
                mutation=101,
                cross=self._cross,
                situation=self._situation,
                elite_num=self._elite_num,
                population=self._population,
                crossover_method=self._crossover_method,
                fitness_function=self._fitness_function
            )
            self.assertEquals(1, -1)
        except TypeError:
            pass

        try:
            # mutation(突然変異のパーセンテージ)は0 ~ 100
            test_ga = ga.GeneticAlgorithm(
                mutation=-1,
                cross=self._cross,
                situation=self._situation,
                elite_num=self._elite_num,
                population=self._population,
                crossover_method=self._crossover_method,
                fitness_function=self._fitness_function
            )
            self.assertEquals(1, -1)
        except TypeError:
            pass

        try:
            # cross(交叉のパーセンテージ)は0 ~ 100
            test_ga = ga.GeneticAlgorithm(
                mutation=self._mutation,
                cross=101,
                situation=self._situation,
                elite_num=self._elite_num,
                population=self._population,
                crossover_method=self._crossover_method,
                fitness_function=self._fitness_function
            )
            self.assertEquals(1, -1)
        except TypeError:
            pass

        try:
            # cross(交叉のパーセンテージ)は0 ~ 100
            test_ga = ga.GeneticAlgorithm(
                mutation=self._mutation,
                cross=-1,
                situation=self._situation,
                elite_num=self._elite_num,
                population=self._population,
                crossover_method=self._crossover_method,
                fitness_function=self._fitness_function
            )
            self.assertEquals(1, -1)
        except TypeError:
            pass

        try:
            # situation(遺伝子の特徴量を表す)はmodules.feature.Situationクラスのインスタンス
            temp_ga = ga.GeneticAlgorithm(
                mutation=self._mutation,
                cross=self._cross,
                situation=[(1, 50), (50, 100), (1, 50)],
                elite_num=self._elite_num,
                population=self._population,
                crossover_method=self._crossover_method,
                fitness_function=self._fitness_function
            )
            self.assertEquals(1, -1)
        except TypeError:
            pass

        try:
            # population(個体数)がelite_num(エリートの個体数)より大きい
            temp_ga = ga.GeneticAlgorithm(
                mutation=self._mutation,
                cross=self._cross,
                situation=self._situation,
                elite_num=101,
                population=100,
                crossover_method=self._crossover_method,
                fitness_function=self._fitness_function
            )
            self.assertEquals(1, -1)
        except ArithmeticError:
            pass

        try:
            # crossover_method(交叉の手法を表す)はmodules.crossover.Crossoverクラスのインスタンス
            test_ga = ga.GeneticAlgorithm(
                mutation=self._mutation,
                cross=self._cross,
                situation=self._situation,
                elite_num=self._elite_num,
                population=self._population,
                crossover_method=100,
                fitness_function=self._fitness_function
            )
            self.assertEquals(1, -1)
        except TypeError:
            pass

        try:
            # fitness_function(適応度関数を表す)はmodules.fitnessfunction.FitnessFunctionクラスのインスタンス
            test_ga = ga.GeneticAlgorithm(
                mutation=self._mutation,
                cross=self._cross,
                situation=self._situation,
                elite_num=self._elite_num,
                population=self._population,
                crossover_method=self._crossover_method,
                fitness_function=100,
            )
            self.assertEquals(1, -1)
        except TypeError:
            pass

    def test_init_population(self):
        """
        遺伝子初期化時に次元が適当かどうかのチェック
        """
        test_ga = ga.GeneticAlgorithm(
            mutation=self._mutation,
            cross=self._cross,
            situation=self._situation,
            elite_num=self._elite_num,
            population=self._population,
            crossover_method=self._crossover_method,
            fitness_function=self._fitness_function,
        )
        result = test_ga.init_population()
        self.assertIsInstance(result, type(np.asarray([1])))
        for i in result:
            self.assertLessEqual(i[0], 50)
            self.assertLessEqual(1, i[0])
            self.assertIsInstance(i, type(np.asarray([])))
        self.assertEqual(self._population, len(result))
        del test_ga

    def test_calc_fitness(self):
        """
        適応度の次元が適当かどうかのチェック
        """
        test_ga = ga.GeneticAlgorithm(
            mutation=self._mutation,
            cross=self._cross,
            situation=self._situation,
            elite_num=self._elite_num,
            population=self._population,
            crossover_method=self._crossover_method,
            fitness_function=self._fitness_function,
        )
        result = test_ga.init_population()
        test_ga.set_geno_type(result)
        fitness = test_ga.calc_fitness(should_log=False)
        fitness_list = list()
        for i in range(self._population):
            fitness_list.append(i + 1)
        test_fitness = np.asarray(fitness_list)
        self.assertEqual(True, np.all(np.equal(test_fitness, fitness)))
        del test_ga

    def test_determine_next_generation(self):
        """
        世代交代で遺伝子の次元が適当どうかチェックする
        """
        # まず初期化する
        test_ga = ga.GeneticAlgorithm(
            mutation=self._mutation,
            cross=self._cross,
            situation=self._situation,
            elite_num=self._elite_num,
            population=self._population,
            crossover_method=self._crossover_method,
            fitness_function=self._fitness_function,
        )
        result = test_ga.init_population()
        test_ga.set_geno_type(result)
        geno_type = test_ga.determine_next_generation()
        self.assertEqual(True, np.all(np.equal(result, geno_type)))

    def test_generation(self):
        # まず初期化する
        test_ga = ga.GeneticAlgorithm(
            mutation=self._mutation,
            cross=self._cross,
            situation=self._situation,
            elite_num=self._elite_num,
            population=self._population,
            crossover_method=self._crossover_method,
            fitness_function=self._fitness_function,
        )
        population_dept = self._db_facade.select_department('populations')
        test_ga.generation(
            steps=20,
            experiment_id=1000,
            log_span=10,
            population_dept=population_dept
        )


class SampleFitnessFunction(fitnessfunction.FitnessFunction):
    """
    テスト用の適応度関数
    """
    def __init__(self, candle_type, db_dept, fitness_function_id):
        super().__init__(candle_type=candle_type, db_dept=db_dept, fitness_function_id=fitness_function_id)

    def calc_fitness(self, geno_type, should_log, population_id):
        if should_log:
            print('** logging **')
        fitness_list = list()
        for i in range(len(geno_type)):
            fitness_list.append(i + 1)
        return np.asarray(fitness_list)


class SampleCrossover(crossover.Crossover):
    """
    テスト用の交叉手法

    """
    def __init__(self, crossover_id):
        super().__init__(crossover_id=crossover_id)

    @classmethod
    def determine_next_generation(cls, geno_type, fitness, situation, mutation, cross, elite_num):
        return geno_type


if __name__ == '__main__':
    unittest.main()
