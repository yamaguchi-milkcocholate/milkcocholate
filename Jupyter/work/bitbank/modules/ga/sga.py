from . import ga
import pprint
import pickle
from modules.fitnessfunction import simple_macd_params


class SimpleGeneticAlgorithm:

    def __init__(self, situation, population=100, mutation=2, cross=70, elite_num=1, candle_type='1hour'):
        self.ga = ga.GeneticAlgorithm(mutation, cross, situation, elite_num=elite_num, population=population)
        self.fitness_function = simple_macd_params.SimpleMacDParams(candle_type)
        self.population = population
        self.situation = situation
        self.geno_type = None
        self.fitness = None

    def __call__(self, steps):
        self.init_population()
        self.generation(steps)

    def init_population(self):
        self.geno_type = self.ga.init_population(self.situation)

    def generation(self, steps):
        self.geno_type, self.fitness = self.ga.generation(steps, self.geno_type, self.fitness_function)
        self.save_geno_type()

    def show_geno_type(self):
        pprint.pprint(self.geno_type)
        print('count: ', len(self.geno_type))

    def show_fitness(self):
        pprint.pprint(self.fitness)
        print('count: ', len(self.fitness))

    def save_geno_type(self):
        save_file = 'geno_type.pkl'
        with open(save_file, 'wb') as f:
            pickle.dump(self.geno_type, f)
        print('saved geno_type')
