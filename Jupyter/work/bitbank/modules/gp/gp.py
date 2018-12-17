import numpy as np
import pickle
import random
from modules.gp.gpgenome import GNPenome
from modules.gp.condition import Condition
from modules.gp.fitnessfunction import *


class GeneticNetwork:

    def __init__(self, mutation, cross, condition, elite_num, population, fitness_function):
        """
        :param mutation:           int                                         突然変異のパーセント
        :param cross:              int                                         交叉のパーセント
        :param condition:          modules.gp.Condition                        特徴量を表す
        :param elite_num:          int                                         エリート個体数
        :param population:         int                                         個体数
        :param fitness_function:   modules.gp.fitnessfunction.FitnessFunction  適応度関数
        """
        # 1. mutation(突然変異のパーセンテージ)は0 ~ 100
        # 2. cross(交叉のパーセンテージ)は0 ~ 100
        # 3. situation(遺伝子の特徴量を表す)はmodules.gp.condition.Conditionクラスのインスタンス
        # 4. population(個体数)がelite_num(エリートの個体数)より大きい
        # 5. fitness_function(適応度関数を表す)はmodules.gp.fitnessfuntion.fitnessfuntion.FitnessFunctionクラスのインスタンス

        if (mutation < 0) or (100 < mutation):
            raise TypeError("mutation must be 0 ~ 100")
        if (cross < 0) or (100 < cross):
            raise TypeError("cross must be - ~ 100")
        if not isinstance(condition, Condition):
            raise TypeError("situation must be an instance of 'Situation'")
        if population < elite_num:
            raise ArithmeticError('population must be larger than elite_num')
        if not isinstance(fitness_function, fitness_function.FitnessFunction):
            raise TypeError("fitness_function must be an instance of 'FitnessFunction'")

        self.__mutation = mutation
        self.__cross = cross
        self.__condition = condition
        self.__elite_num = elite_num
        self.__population = population
        self.__fitness_function = fitness_function
        self.genome = None
        self.fitness = None

    def init_population(self):
        """
        遺伝子の初期化(乱数)
        """
        pass

    def generation(self, steps, experiment_id, log_span, population_dept):
        """
        世代交代
        :param steps:            int
        :param experiment_id:    int
        :param log_span:         int
        :param population_dept:  modules.db.popdept.PopulationDepartment
        """
        self.init_population()
        self.calc_fitness()
        for step_i in range(steps + 1):
            print('No, ', step_i)
            self.determine_next_generation()
            if step_i % log_span is 0:
                # 記録を取る
                population_id = self.__log_population(
                    experiment_id=experiment_id,
                    step_i=step_i,
                    population_dept=population_dept
                )
                # 適応度計算時に記録を取る
                self.calc_fitness(population_id=population_id, is_log=True)
            else:
                self.calc_fitness()

    def calc_fitness(self, population_id=0, is_log=False):
        """
        適応度関数に適応度を計算させる
        :param population_id: int   テーブル'populations'のid
        :param is_log:        bool  ログを記録するかどうか
        """
        self.fitness = self.__fitness_function.calc_fitness(
            genome=self.genome,
            population_id=population_id,
            is_log=is_log
        )

    def determine_next_generation(self):
        """
        次の世代を決定する
        """
        pass

    def __log_population(self, experiment_id, step_i, population_dept):
        """
        テーブル'populations'に書き込む
        :param experiment_id:
        :param step_i:
        :param population_dept:
        :return population_id:    int    テーブル'populations'に書きこんだid
        """
        population_id = population_dept.make_writer_find_next_id()
        population_dept.give_writer_task(values=[
            [
                experiment_id,
                step_i,
                pickle.dumps(self.genome),
                pickle.dumps(self.fitness),
            ],
        ])
        return population_id
