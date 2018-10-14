# coding:utf-8
import numpy as np
import random
import pickle
import pprint
import os
from modules.feature import genofeature


class GeneticAlgorithm:
    EXPERIMENT_TABLE = 'experiments'
    POPULATION_TABLE = 'populations'
    LOG_TABLE = 'logs'

    def __init__(self, mutation, cross, situation, elite_num, population):
        """
        :param mutation:    int        突然変異が起きるパーセンテージ
        :param cross:       int        交叉を起こすパーセンテージ
        :param situation:   Situation  特徴量の情報を持つクラスのインスタンス
        :param elite_num:   int        次の世代に残すエリートの個体数
        :param population:  int        個体数
        """
        self.mutation = mutation
        self.cross = cross
        if not isinstance(situation, genofeature.Situation):
            raise TypeError("situation must be an instance of 'Situation'")
        self.situation = situation
        if population < elite_num:
            raise ArithmeticError('population must be larger than elite_num')
        self.population = population
        self.elite_num = elite_num
        self.geno_type = None
        self.fitness = None
        self._log_span = None
        self._experiment_id = None
        self._db_facade = None

    def log_setting(self, db_facade, log_span):
        self._db_facade = db_facade
        dept = self._db_facade.select_department(self.EXPERIMENT_TABLE)
        self._experiment_id = dept.make_writer_find_next_id()
        self._log_span = log_span

    def init_population(self):
        """
        遺伝子の初期化
        :return: numpy 初期化された遺伝子
        """
        pop_list = []
        for pop_i in range(self.population):
            inter_list = []
            range_tuple_list = self.situation.range_to_tuple_list()
            for situ_i in range(len(range_tuple_list)):
                value = range_tuple_list[situ_i]
                inter_list.append(random.randint(value[0], value[1]))
            pop_list.append(np.asarray(inter_list, int))
        return np.asarray(pop_list, int)

    def generation(self, steps, geno_type, fitness_function, selected_ga):
        """
        世代数だけ世代交代させる
        :param steps:              int                            世代交代数
        :param geno_type:          numpy                          遺伝子
        :param fitness_function:   fitnessfunction                適応度関数をもつクラスのインスタンス
        :param selected_ga:        object                         交叉方法の違いなどで分類される遺伝的アルゴリズムのクラスのインスタンス
        :return:                   numpy, numpy                   遺伝子, 適応度
        """
        fitness = self.calc_fitness(geno_type, fitness_function)
        for step_i in range(steps):
            print('No. ', step_i + 1)
            geno_type = selected_ga.determine_next_generation(geno_type, fitness)
            if step_i % self._log_span is 0:
                fitness = self.calc_fitness(geno_type, fitness_function)
                self._log_population(generation_number=step_i, geno_type=geno_type, fitness=fitness)
            else:
                fitness = self.calc_fitness(geno_type, fitness_function)
        self.geno_type = geno_type
        self.fitness = fitness
        self.show_geno_type()
        self.show_geno_type()
        return geno_type, fitness

    def select_elites(self, geno_type, fitness):
        """
        エリート個体の遺伝子を返す
        :param fitness:     numpy 適応度
        :param geno_type    numpy 遺伝子
        :return:            numpy エリート個体の遺伝子
        """
        fitness = np.argsort(fitness)[::-1]
        elites = geno_type[fitness[:self.elite_num]]
        return elites

    @staticmethod
    def calc_fitness(geno_type, fitness_function):
        """
        適応度関数に適応度を計算させ、その値を返す
        :param geno_type:           numpy     遺伝子
        :param fitness_function:    object    適応度関数を持つクラスのインスタンス
        :return:                    numpy     適応度
        """
        fitness = fitness_function.calc_fitness(geno_type)
        return fitness

    @staticmethod
    def save_geno_type(geno_type):
        """
        遺伝子をpickleファイルに保存する
        Todo: 📁 resultにテクニカル分析手法や遺伝的アルゴリズム別で保存する
        :param geno_type:      numpy  遺伝子
        :return:
        """
        save_file = os.path.dirname(os.path.dirname(__file__) + '/../../results/') + '/geno_type.pkl'
        with open(save_file, 'wb') as f:
            pickle.dump(geno_type, f)
        print('saved geno_type')

    def show_geno_type(self):
        pprint.pprint(self.geno_type)
        print('count: ', len(self.geno_type))

    def show_fitness(self):
        pprint.pprint(self.fitness)
        print('count: ', len(self.fitness))

    def _log_population(self, generation_number, geno_type, fitness):
        """
        テーブル'populations'に書き込むメソッド
        :param generation_number: int   書き込む個体の世代数
        :param geno_type:         numpy 遺伝子
        :param fitness:           numpy 適応度
        """
        dept = self._db_facade.select_department(self.POPULATION_TABLE)
        dept.give_writer_task(values=[
            [
                self._experiment_id,
                generation_number,
                pickle.dumps(geno_type),
                pickle.dumps(fitness),
            ],
        ])
