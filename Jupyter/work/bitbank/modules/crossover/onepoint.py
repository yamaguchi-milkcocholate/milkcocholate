from modules.ga import go
import numpy as np
import random


class OnePointCrossover(go.Crossover):
    """
    一点交叉を行う
    """
    @classmethod
    def determine_next_generation(cls, geno_type, fitness, situation, mutation, cross, elite_num):
        """
        次の世代を決定する
        :param   geno_type: numpy      遺伝子
        :param   fitness:   numpy      適応度
        :param   situation  Situation  遺伝子の特徴量を表すクラスのインスタンス
        :param   mutation   int        突然変異を起こすパーセンテージ
        :param   cross      int        交叉が起きるパーセンテージ
        :param   elite_num  int        次の世代に残すエリート個体の数
        :return: geno_type  numpy      遺伝子
        """
        sum_fitness = 0
        population = geno_type.shape[0]
        feature_num = geno_type.shape[1]
        field = []
        for pop_i in range(population):
            sum_fitness += fitness[pop_i]
            field.append(sum_fitness)
        field = np.asarray(field, int)
        new_geno_type = np.empty((0, feature_num), int)
        elites = cls.select_elites(elite_num=elite_num, geno_type=geno_type, fitness=fitness)

        for geno_i in range(0, population):
            roulette = random.randrange(0, sum_fitness)
            select_index = np.where(field >= roulette)
            new_geno_type = np.r_[new_geno_type, geno_type[select_index[0][:1]]]

        for geno_i in range(0, population - population % 2, 2):
            rand = random.randrange(0, 100)
            if rand >= cross:
                continue
            pair_i = geno_i + 1
            cut_point = random.randrange(0, feature_num - 1)
            geno_type[geno_i] = np.asarray(np.r_[new_geno_type[geno_i][:cut_point + 1],
                                                 new_geno_type[pair_i][cut_point + 1:]], int)
            geno_type[pair_i] = np.asarray(np.r_[new_geno_type[pair_i][:cut_point + 1],
                                                 new_geno_type[geno_i][cut_point + 1:]], int)

        range_tuple_list = situation.range_to_tuple_list()
        for geno_i in range(elite_num, population):
            for situ_i in range(feature_num):
                rand = random.randrange(0, 100)
                if rand >= mutation:
                    continue
                value = range_tuple_list[situ_i]
                geno_type[geno_i][situ_i] = random.randrange(value[0], value[1])

        rest = geno_type[elite_num:]
        geno_type = np.asarray(np.r_[elites, rest], int)
        return geno_type

    @staticmethod
    def select_elites(elite_num, geno_type, fitness):
        elites = super().select_elites(elite_num=elite_num, geno_type=geno_type, fitness=fitness)
        return elites
