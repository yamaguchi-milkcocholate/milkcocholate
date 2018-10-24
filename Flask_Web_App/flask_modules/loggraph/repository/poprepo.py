from flask_modules.db import reader
from flask_modules.loggraph import pop
import pickle


class PopulationRepository:
    POPULATIONS_TABLE = 'populations'

    def __init__(self, host):
        self._reader = reader.Reader(host=host)

    def get_populations(self, experiment_id):
        result = self._reader(
            table=self.POPULATIONS_TABLE
        ).select().where(['experiment_id', '=', experiment_id]).get()
        population_list = list()
        for result_i in range(len(result)):
            genome = pickle.loads(result[result_i]['genome'])
            fitness = pickle.loads(result[result_i]['fitness'])
            population = pop.Population(
                population_id=result[result_i]['id'],
                experiment_id=result[result_i]['experiment_id'],
                generation_number=result[result_i]['generation_number'],
                genome=genome,
                fitness=fitness
            )
            population_list.append(population)

        return population_list
