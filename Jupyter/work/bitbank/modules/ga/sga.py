from . import ga


class SimpleGeneticAlgorithm(ga.GeneticAlgorithm, type='sga'):

    def __init__(self, situation, action, population):
        super().__init__(situation, action, population)

    def init_population(self):
        pass

    def generation(self, steps):
        pass

    def calc_fitness(self, steps):
        pass

    def determine_next_generation(self):
        pass

    def obtain_situation(self):
        pass
