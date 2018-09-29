from . import ga
import pprint
import pickle
import numpy as np
import random


class SimpleGeneticAlgorithm:

    def __init__(self, situation, fitness_function, population=100, mutation=2, cross=70, elite_num=1):
        self.ga = ga.GeneticAlgorithm(mutation, cross, situation, elite_num=elite_num, population=population)
        self.fitness_function = fitness_function
        self.population = population
        self.situation = situation
        self.cross = cross
        self.mutation = mutation
        self.elite_num = elite_num
        self.geno_type = None
        self.fitness = None

    def __call__(self, steps):
        self.init_population()
        self.generation(steps)

    def init_population(self):
        self.geno_type = self.ga.init_population()

    def generation(self, steps):
        self.geno_type, self.fitness = self.ga.generation(steps, self.geno_type, self.fitness_function, self)

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
        elites = self.ga.select_elites(geno_type, fitness)

        for geno_i in range(0, population):
            roulette = random.randrange(0, sum_fitness)
            select_index = np.where(field >= roulette)
            new_geno_type = np.r_[new_geno_type, geno_type[select_index[0][:1]]]

        for geno_i in range(0, population - population % 2, 2):
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

    def save_geno_type(self):
        fitness_function = self.fitness_function.__class__.__name__
        ga_name = self.__class__.__name__
        save_file = 'geno_type_'+ga_name+'_'+fitness_function+'.pkl'
        with open(save_file, 'wb') as f:
            pickle.dump(self.geno_type, f)
        print('saved geno_type')
