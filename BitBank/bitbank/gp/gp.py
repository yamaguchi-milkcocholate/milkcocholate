import numpy as np
import random
from bitbank.gp.gpgenome import GPGenome
from bitbank.gp.fitnessfunction.fitnessfunction import FitnessFunction
from bitbank.exceptions.gpexception import NodeException
import copy


class GeneticNetwork:
    MUTATION_NUM = 5

    def __init__(self, mutation, cross, elite_num, new_num, population, fitness_function):
        """
        :param mutation:           int                                         突然変異のパーセント
        :param cross:              int                                         交叉のパーセント
        :param elite_num:          int                                         エリート個体数
        :param new_num:            int                                         新規個体数
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
        if population < elite_num:
            raise ArithmeticError('population must be larger than elite_num')
        if not isinstance(fitness_function, FitnessFunction):
            raise TypeError("fitness_function must be an instance of 'FitnessFunction'")

        self.__mutation = mutation
        self.__cross = cross
        self.__elite_num = elite_num
        self.__new_num = new_num
        self.__population = population
        self.__fitness_function = fitness_function
        self.__condition = self.__fitness_function.get_condition()
        self.genomes = list()
        self.fitness = None

    def genome_normalization(self):
        """
        遺伝子を正規化
        :return:
        """
        for i in range(len(self.genomes)):
            self.genomes[i].normalization()

    def init_population(self):
        """
        遺伝子の初期化(乱数)
        GPGenomeに木を生成させる
        """
        for i in range(self.__population):
            self.genomes.append(GPGenome(condition=self.__condition))
        self.genome_normalization()

    def generation(self, steps):
        """
        世代交代
        :param steps:            int
        """
        self.init_population()
        self.calc_fitness()
        for step_i in range(steps + 1):
            print('No, ', step_i)
            self.determine_next_generation()
            self.calc_fitness()

    def calc_fitness(self):
        """
        適応度関数に適応度を計算させる
        """
        self.fitness = self.__fitness_function.calc_fitness(
            genomes=self.genomes,
        )

    def determine_next_generation(self):
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
        for geno_i in range(0, len(self.genomes) - self.__elite_num - self.__new_num, 2):
            par_a, par_b = self.roulette_select(roulette=roulette, sum_fitness=sum_fitness)
            child_a, child_b = self.crossover(par_a, par_b)
            new_genomes.append(child_a)
            new_genomes.append(child_b)

        # 新規個体
        for i in range(0, self.__new_num):
            new_genomes.append(GPGenome(condition=self.__condition))

        # 突然変異
        for new_genome in new_genomes:
            if random.randint(0, 100) <= self.__mutation:
                for i in range(self.MUTATION_NUM):
                    try:
                        new_genome.mutate()
                    except NodeException as ne:
                        new_genome.show_tree()
                        raise ne

        # エリートを結合
        new_genomes[0:0] = elites
        self.genomes = new_genomes
        self.genome_normalization()

    def roulette_select(self, roulette, sum_fitness):
        """
        ルーレット選択する
        :return: GPGenome, GPGenome
        """
        # rouletteはソートされている。要素がしきい値をちょうど越える時のインデックスを取る
        par_a = self.genomes[np.where(roulette >= random.uniform(0, sum_fitness))[0][0]]
        par_b = self.genomes[np.where(roulette >= random.uniform(0, sum_fitness))[0][0]]
        return copy.deepcopy(par_a), copy.deepcopy(par_b)

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
        node_id_a = node_a.get_node_id()
        node_id_b = node_b.get_node_id()
        try:
            a.put_node(node=node_b, node_id=node_id_a)
            b.put_node(node=node_a, node_id=node_id_b)
        except NodeException as ne:
            print('tree_a:------------------------------------')
            a.show_tree()
            print("id(a) = %i" % id(a))
            print('tree_b:------------------------------------')
            b.show_tree()
            print("id(b) = %i" % id(b))
            print('node_a:------------------------------------')
            node_a.show_node()
            print(node_a.get_node_id())
            print("id(node_a) = %i" % id(node_a))
            print('node_b-------------------------------------')
            node_b.show_node()
            print(node_b.get_node_id())
            print("id(node_b) = %i" % id(node_b))
            print(ne)
            raise ne
        return copy.deepcopy(a), copy.deepcopy(b)

    def select_elites(self):
        fitness = np.argsort(self.fitness)[::-1]
        fitness = fitness[:self.__elite_num]
        elites = list()
        for i in range(len(fitness)):
            elites.append(self.genomes[fitness[i]])
        return copy.deepcopy(elites)

    def show_genomes(self):
        for i in range(len(self.genomes)):
            self.genomes[i].show_tree()
            print()

    def get_elite_genome(self):
        return self.genomes[0]
