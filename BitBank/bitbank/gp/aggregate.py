from bitbank.gp.gp import GeneticNetwork


class Aggregate:

    def __init__(self, gp_num, mutation, cross, elite_num, new_num, population, fitness_function, keep, depth, steps):
        self.gp_num = gp_num
        self.mutation = mutation
        self.cross = cross
        self.elite_num = elite_num
        self.new_num = new_num
        self.population = population
        self.fitness_function = fitness_function
        self.keep = keep
        self.depth = depth
        self.steps = steps
        self.gps = None
        self.aggregated_gp = None
        self.__train_gps()
        self.__aggregate()

    def __train_gps(self):
        gps = list()
        for i in range(self.gp_num):
            gp = GeneticNetwork(
                mutation=self.mutation,
                cross=self.cross,
                elite_num=self.elite_num,
                new_num=self.new_num,
                population=self.population,
                fitness_function=self.fitness_function,
                keep=self.keep,
                depth=self.depth
            )
            gp.generation(steps=self.steps)
            gps.append(gp)
        self.gps = gps

    def __aggregate(self):
        genomes = list()
        for i in range(self.gp_num):
            genomes.append(self.gps[i].genomes[0])
        self.aggregated_gp = GeneticNetwork(
            mutation=self.mutation,
            cross=self.cross,
            elite_num=self.elite_num,
            new_num=self.new_num,
            population=self.population,
            fitness_function=self.fitness_function,
            keep=self.keep,
            depth=self.depth
        )
        self.aggregated_gp.aggregate(genomes=genomes, steps=self.steps)

    def get_elite_genome(self):
        return self.aggregated_gp.get_elite_genome()
