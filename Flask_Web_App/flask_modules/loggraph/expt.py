class Experiment:

    def __init__(self, experiment_id, crossover_name, fitness_function_name, situation, hyper_params,
                 mutation_rate, cross_rate, population, elite_num, start_time, end_time, execute_time):
        self.id = experiment_id
        self.crossover_name = crossover_name
        self.fitness_function_name = fitness_function_name
        self.situation = situation
        self.hyper_params = hyper_params
        self.mutation_rate = mutation_rate
        self.cross_rate = cross_rate
        self.population = population
        self.elite_num = elite_num
        self.start_time = start_time
        self.end_time = end_time
        self.execute_time = execute_time
