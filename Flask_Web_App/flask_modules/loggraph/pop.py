class Population:

    def __init__(self, population_id, experiment_id, generation_number, genome, fitness):
        """
        :param population_id: int
        :param experiment_id: int
        :param genome:        numpy
        :param fitness:       numpy
        """
        self.id = population_id
        self.experiment_id = experiment_id
        self.generation_number = generation_number
        self.genome = genome
        self.fitness = fitness
