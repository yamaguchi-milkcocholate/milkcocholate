

class Situation:

    def __init__(self):
        self._fitness_function_id = None
        self._genomes = list()
        self._genome_ranges = dict()

    def set_fitness_function_id(self, id):
        self._fitness_function_id = id

    def set_genome_ranges(self, **kwargs):
        for key in kwargs:
            self._genomes.append(key)
        self._genome_ranges = kwargs

    def get_fitness_function(self):
        return self._fitness_function_id

    def get_genomes(self):
        return self._genomes

    def get_genome_ranges(self):
        return self._genome_ranges

    def range_to_tuple_list(self):
        tuple_list = list()
        for key in self._genome_ranges:
            tuple_list.append(self._genome_ranges[key])
