import numpy as np
import random
import pickle
from modules.feature import genofeature
from modules.crossover import crossover
from modules.fitnessfunction import fitnessfunction


class GeneticAlgorithm:

    def __init__(self, mutation, cross, situation, elite_num, population, crossover_method, fitness_function):
        """
        :param mutation:         int               突然変異が起きるパーセンテージ
        :param cross:            int               交叉を起こすパーセンテージ
        :param situation:        Situation         特徴量の情報を持つクラスのインスタンス
        :param elite_num:        int               次の世代に残すエリートの個体数
        :param population:       int               個体数
        :param crossover_method: Crossover         交叉の手法を表すクラスのインスタンス
        :param fitness_function  FitnessFunction   適応度関数を表すクラスのインスタンス
        """
        # 1. mutation(突然変異のパーセンテージ)は0 ~ 100
        # 2. cross(交叉のパーセンテージ)は0 ~ 100
        # 3. situation(遺伝子の特徴量を表す)はmodules.feature.Situationクラスのインスタンス
        # 4. population(個体数)がelite_num(エリートの個体数)より大きい
        # 5. crossover_method(交叉の手法を表す)はmodules.crossover.Crossoverクラスのインスタンス
        # 6. fitness_function(適応度関数を表す)はmodules.fitnessfunction.FitnessFunctionクラスのインスタンス
        if (mutation < 0) or (100 < mutation):
            raise TypeError("mutation must be 0 ~ 100")
        if (cross < 0) or (100 < cross):
            raise TypeError("cross must be - ~ 100")
        if not isinstance(situation, genofeature.Situation):
            raise TypeError("situation must be an instance of 'Situation'")
        if population < elite_num:
            raise ArithmeticError('population must be larger than elite_num')
        if not isinstance(crossover_method, crossover.Crossover):
            raise TypeError("crossover_method must be an instance of 'Crossover'")
        if not isinstance(fitness_function, fitnessfunction.FitnessFunction):
            raise TypeError("fitness_function must be an instance of 'FitnessFunction'")
        self._mutation = mutation
        self._cross = cross
        self._situation = situation
        self._elite_num = elite_num
        self._population = population
        self._crossover = crossover_method
        self._fitness_function = fitness_function
        self._geno_type = None
        self._fitness = None

    def init_population(self):
        """
        遺伝子の初期化
        :return geno_type  numpy 遺伝子
        """
        pop_list = []
        for pop_i in range(self._population):
            inter_list = []
            range_tuple_list = self._situation.range_to_tuple_list()
            for situ_i in range(len(range_tuple_list)):
                value = range_tuple_list[situ_i]
                inter_list.append(random.randint(value[0], value[1]))
            pop_list.append(np.asarray(inter_list, int))
        return np.asarray(pop_list, int)

    def generation(self, steps, experiment_id, log_span, population_dept):
        """
        世代数だけ世代交代させる
        :param steps:              int                  世代交代数
        :param experiment_id:      int                  テーブル'experiments'のid
        :param log_span:           int                  記録をどれくらいの期間ごとに取るか
        :param population_dept:    PopulationDepartment テーブル'population'のDB操作をするクラスのインスタンス
        :return:                   numpy, numpy         遺伝子, 適応度
        """
        self._geno_type = self.init_population()
        self._fitness = self.calc_fitness(should_log=False)
        for step_i in range(steps):
            print('No. ', step_i)
            self._geno_type = self.determine_next_generation()
            if step_i % log_span is 0:
                # 記録を取る
                # populationsに書き込む
                population_id = self._log_population(
                    experiment_id=experiment_id,
                    generation_number=step_i,
                    geno_type=self._geno_type,
                    fitness=self._fitness,
                    population_dept=population_dept)
                # 適応度計算時に記録を取るようにする
                self._fitness = self.calc_fitness(should_log=True, population_id=population_id)
            else:
                self._fitness = self.calc_fitness(should_log=False)

    def determine_next_generation(self):
        """
        次の世代を決定する
        :return: geno_type numpy 遺伝子
        """
        geno_type = self._crossover.determine_next_generation(
            geno_type=self._geno_type, fitness=self._fitness, situation=self._situation,
            mutation=self._mutation, cross=self._cross, elite_num=self._elite_num
        )
        return geno_type

    def calc_fitness(self, should_log, population_id=0):
        """
        適応度関数に適応度を計算させ、その値を返す
        :param should_log:      bool  ログを記録するかどうか
        :param population_id:   int   テーブル'experiments'のid
        :return: fitness:       numpy 適応度
        """
        fitness = self._fitness_function.calc_fitness(
            self._geno_type, should_log=should_log, population_id=population_id)
        return fitness

    @staticmethod
    def _log_population(experiment_id, generation_number, geno_type, fitness, population_dept):
        """
        テーブル'populations'に書き込むメソッド
        :param experiment_id:     int                   テーブル'experiments'のid
        :param generation_number: int                   書き込む個体の世代数
        :param geno_type:         numpy                 遺伝子
        :param fitness:           numpy                 適応度
        :param population_dept:   PopulationDepartment  テーブル'populations'へのDB操作を扱かうクラスのインスタンス
        :return population_id:    int                   テーブル'populations'に書きこんだid
        """
        population_id = population_dept.make_writer_find_next_id()
        population_dept.give_writer_task(values=[
            [
                experiment_id,
                generation_number,
                pickle.dumps(geno_type),
                pickle.dumps(fitness),
            ],
        ])
        return population_id

    def get_mutation(self):
        return self._mutation

    def get_cross(self):
        return self._cross

    def get_situation(self):
        return self._situation

    def get_elite_num(self):
        return self._elite_num

    def get_population(self):
        return self._population

    def get_crossover_id(self):
        return self._crossover.get_crossover_id()

    def get_fitness_function_id(self):
        return self._fitness_function.get_fitness_function_id()

    def get_geno_type(self):
        return self._geno_type

    def get_fitness(self):
        return self._fitness

    def set_geno_type(self, geno_type):
        self._geno_type = geno_type

    def set_fitness(self, fitness):
        self._fitness = fitness
