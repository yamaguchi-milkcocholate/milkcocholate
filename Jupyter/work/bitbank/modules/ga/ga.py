import numpy as np
import random
import pickle


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
        if (population + elite_num) % 2 is not 0:
            raise ArithmeticError('population + elite_num is must be even')
        self.population = population
        self.elite_num = elite_num

    def init_population(self):
        """
        :return: numpy
        """
        pop_list = []
        for pop_i in range(self.population):
            inter_list = []
            for situ_i in range(len(self.situation)):
                value = self.situation[situ_i]
                inter_list.append(random.randint(value[0], value[1]))
            pop_list.append(np.asarray(inter_list, int))
        return np.asarray(pop_list, int)

    def generation(self, steps, geno_type, fitness_function):
        """
        :param steps: int
        :param geno_type: numpy
        :param fitness_function: fitnessfunction
        :return:
        """
        fitness = self.calc_fitness(geno_type, fitness_function)
        for step_i in range(steps):
            print('No. ', step_i + 1)
            geno_type = self.determine_next_generation(geno_type, fitness)
            fitness = self.calc_fitness(geno_type, fitness_function)
            self.save_geno_type(geno_type)
        return geno_type, fitness

    @staticmethod
    def calc_fitness(geno_type, fitness_function):
        fitness = fitness_function.calc_fitness(geno_type)
        return fitness

    def determine_next_generation(self, geno_type, fitness):
        sum_fitness = 0
        population = geno_type.shape[0]
        situations = geno_type.shape[1]
        field = []
        for pop_i in range(population):
            sum_fitness += fitness[pop_i]
            field.append(sum_fitness)
        field = np.asarray(field, int)
        new_geno_type = np.empty((0, situations), int)
        elites = self.select_elites(geno_type, fitness)

        for geno_i in range(0, population):
            roulette = random.randrange(0, sum_fitness)
            select_index = np.where(field >= roulette)
            new_geno_type = np.r_[new_geno_type, geno_type[select_index[0][:1]]]

        for geno_i in range(0, population, 2):
            rand = random.randrange(0, 100)
            if rand >= self.cross:
                continue
            pair_i = geno_i + 1
            cut_point = random.randrange(0, situations - 1)
            geno_type[geno_i] = np.asarray(np.r_[new_geno_type[geno_i][:cut_point + 1],
                                                 new_geno_type[pair_i][cut_point + 1:]], int)
            geno_type[pair_i] = np.asarray(np.r_[new_geno_type[pair_i][:cut_point + 1],
                                                 new_geno_type[geno_i][cut_point + 1:]], int)

        for geno_i in range(self.elite_num, population):
            for situ_i in range(situations):
                rand = random.randrange(0, 100)
                if rand >= self.mutation:
                    continue
                value = self.situation[situ_i]
                geno_type[geno_i][situ_i] = random.randrange(value[0], value[1])

        rest = geno_type[self.elite_num:]
        geno_type = np.asarray(np.r_[elites, rest], int)
        return geno_type

    def select_elites(self, geno_type, fitness):
        """
        :param fitness: numpy
        :param geno_type numpy
        :return: numpy
        """
        fitness = np.argsort(fitness)[::-1]
        elites = geno_type[fitness[:self.elite_num]]
        return elites

    @staticmethod
    def save_geno_type(geno_type):
        save_file = 'geno_type.pkl'
        with open(save_file, 'wb') as f:
            pickle.dump(geno_type, f)
        print('saved geno_type')
