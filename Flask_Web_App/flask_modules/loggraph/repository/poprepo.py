from flask_modules.loggraph import pop
from flask_modules.loggraph.repository import repository
import pickle


class PopulationRepository(repository.Repository):
    POPULATIONS_TABLE = 'populations'

    def __init__(self, host):
        super().__init__(host=host)

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
