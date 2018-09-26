import numpy as np
import random


class GeneticAlgorithm:

    def __init__(self, mutation, cross, situation, elite_num):
        self.mutation = mutation
        self.cross = cross
        self.situation = situation
        self.elite_num = elite_num

    @staticmethod
    def init_population(situation, population):
        """
        :param situation: dict(tuple)
        :param population: int
        :return: numpy
        """
        pop_list = []
        for pop_i in range(population):
            inter_list = []
            for situ_i in range(len(situation)):
                value = situation[situ_i]
                inter_list.append(random.randint(value[0], value[1]))
            pop_list.append(np.asarray(inter_list, int))
        return np.asarray(pop_list, int)

    def generation(self, steps, geno_type, fitness_function):
        """

        :param steps: int
        :param geno_type: numpy
        :param fitness: numpy
        :param fitness_function: fitnessfunction
        :return:
        """
        fitness = self.calc_fitness(geno_type, fitness_function)
        for step_i in range(steps):
            print('No. ', step_i + 1)
            geno_type = self.determine_next_generation(geno_type, fitness, self.elite_num)
            fitness = self.calc_fitness(geno_type, fitness_function)
        return geno_type, fitness

    @staticmethod
    def calc_fitness(geno_type, fitness_function):
        fitness = fitness_function.calc_fitness(geno_type)
        return fitness

    def determine_next_generation(self, geno_type, fitness, elite_num):
        sum_fitness = 0
        population = geno_type.shape[0]
        situations = geno_type.shape[1]
        field = []
        for pop_i in range(population):
            sum_fitness += fitness[pop_i]
            field.append(fitness[pop_i])
        field = np.asarray(field, int)
        new_geno_type = np.empty((0, situations), int)
        elites = self.select_elites(geno_type, fitness, elite_num)

        for geno_i in range(elite_num, population):
            roulette = random.randrange(0, sum_fitness)
            select_index = np.where(field >= roulette)[0]
            new_geno_type = np.append(new_geno_type, geno_type[select_index])

        for geno_i in range(elite_num, population, 2):
            rand = random.randrange(0, 100)
            if rand >= self.cross:
                continue
            pair_i = geno_i + 1
            cut_point = random.randrange(0, situations - 1)
            geno_type[geno_i] = np.asarray(np.r_[new_geno_type[geno_i][:cut_point],
                                                 new_geno_type[pair_i][cut_point + 1:]], int)
            geno_type[pair_i] = np.asarray(np.r_[new_geno_type[pair_i][:cut_point],
                                                 new_geno_type[geno_i][cut_point + 1:]], int)

        for geno_i in range(elite_num, population):
            for situ_i in range(situations):
                rand = random.randrange(0, 100)
                if rand >= self.mutation:
                    continue
                value = self.situation[situ_i]
                geno_type[geno_i][situ_i] = random.randrange(value[0], value[1])

        rest = geno_type[elite_num:]
        geno_type = np.asarray(np.r_[elites, rest], int)
        return geno_type

    @staticmethod
    def select_elites(geno_type, fitness, num):
        """

        :param num: int
        :param fitness: numpy
        :param geno_type numpy
        :return: numpy
        """
        fitness = np.argsort(fitness)[::-1]
        elites = geno_type[fitness[:num]]
        return elites
