import numpy as np
import pickle
import random
from modules.gp.gpgenome import GPGenome
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
        self.genomes = None
        self.fitness = None

    def init_population(self):
        """
        遺伝子の初期化(乱数)
        GPGenomeに木を生成させる
        """
        for i in range(self.__population):
            self.genomes.append(GPGenome(condition=self.__condition))

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
            genomes=self.genomes,
            population_id=population_id,
            is_log=is_log
        )

    # def determine_next_generation(self):
        """
        次の世代を決定する
        """
        sum_fitness = 0
        roulette = list()
        # 総和とルーレットをつくる
        for fitness in self.fitness:
            sum_fitness += fitness
            roulette.append(sum_fitness)
        roulette = np.asarray(roulette)
        # 次世代の遺伝子リスト
        new_genomes = list()
        elites = self.select_elites()

        # エリート以外の遺伝子を交叉
        for geno_i in range(len(self.genomes) - self.__elite_num):
            par_a, par_b = self.roulette_select(roulette=roulette, sum_fitness=sum_fitness)
            child_a, child_b = self.crossover(par_a, par_b)
            new_genomes.append(child_a)
            new_genomes.append(child_b)

        # 突然変異
        for new_genome in new_genomes:
            # 何回の突然変異を起こすか
            count = int(self.__mutation * new_genome.get_total())
            for i in range(count):
                new_genome.mutate()

        # エリートを結合
        new_genomes[0:0] = elites
        self.genomes = new_genomes

    def roulette_select(self, roulette, sum_fitness):
        """
        ルーレット選択する
        :return: GPGenome, GPGenome
        """
        # rouletteはソートされている。要素がしきい値をちょうど越える時のインデックスを取る
        par_a = self.genomes[np.where(roulette >= random.randrange(0, sum_fitness))[0]]
        par_b = self.genomes[np.where(roulette >= random.randrange(0, sum_fitness))[0]]
        return par_a, par_b

    @staticmethod
    def crossover(a, b):
        """
        交叉させて子の遺伝子を返す
        :param a: GPGenome
        :param b: GPGenome
        :return: GPGenome
        """
        node_a = a.random_node()
        node_b = b.random_node()
        a.put_node(node=node_b, node_id=node_a.get_node_id())
        b.put_node(node=node_a, node_id=node_b.get_node_id())
        return a, b

    def select_elites(self):
        fitness = np.argsort(self.fitness)[::-1]
        elites = self.genomes[fitness[:self.__elite_num]]
        return elites

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
                pickle.dumps(self.genomes),
                pickle.dumps(self.fitness),
            ],
        ])
        return population_id
