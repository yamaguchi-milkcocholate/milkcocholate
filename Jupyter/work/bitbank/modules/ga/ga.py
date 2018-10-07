# coding:utf-8
import numpy as np
import random
import pickle
import pprint
import os


class GeneticAlgorithm:

    def __init__(self, mutation, cross, situation, elite_num, population):
        self.mutation = mutation
        self.cross = cross
        for i in situation:
            if type(i) is not tuple:
                raise TypeError('need tuple')
        self.situation = situation
        if population < elite_num:
            raise ArithmeticError('population must be larger than elite_num')
        self.population = population
        self.elite_num = elite_num
        self.geno_type = None
        self.fitness = None

    def init_population(self):
        """
        遺伝子の初期化
        :return: numpy 初期化された遺伝子
        """
        pop_list = []
        for pop_i in range(self.population):
            inter_list = []
            for situ_i in range(len(self.situation)):
                value = self.situation[situ_i]
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
            fitness = self.calc_fitness(geno_type, fitness_function)
            self.save_geno_type(geno_type)
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
