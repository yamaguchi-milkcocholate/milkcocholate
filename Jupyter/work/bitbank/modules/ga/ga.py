import numpy as np
import random
import pickle
import pprint


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

    def generation(self, steps, geno_type, fitness_function, selected_ga):
        """
        :param steps: int
        :param geno_type: numpy
        :param fitness_function: fitnessfunction
        :param selected_ga: object
        :return: numpy.adarray, numpy. adarray
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
        :param fitness: numpy
        :param geno_type numpy
        :return: numpy
        """
        fitness = np.argsort(fitness)[::-1]
        elites = geno_type[fitness[:self.elite_num]]
        return elites

    @staticmethod
    def calc_fitness(geno_type, fitness_function):
        fitness = fitness_function.calc_fitness(geno_type)
        return fitness

    @staticmethod
    def save_geno_type(geno_type):
        save_file = 'geno_type.pkl'
        with open(save_file, 'wb') as f:
            pickle.dump(geno_type, f)
        print('saved geno_type')

    def show_geno_type(self):
        pprint.pprint(self.geno_type)
        print('count: ', len(self.geno_type))

    def show_fitness(self):
        pprint.pprint(self.fitness)
        print('count: ', len(self.fitness))
