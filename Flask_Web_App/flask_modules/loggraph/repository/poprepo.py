from flask_modules.loggraph import pop
from flask_modules.loggraph.repository import repository
from flask_modules.exceptions.dbhost import HostNotFoundException
import pickle


class PopulationRepository(repository.Repository):
    POPULATIONS_TABLE = 'populations'

    def __init__(self, host):
        super().__init__(host=host)

    def get_populations(self, experiment_id):
        try:
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
        except HostNotFoundException:
            raise

    def get_population(self, population_id):
        try:
            result = self._reader(
                table=self.POPULATIONS_TABLE
            ).find(search_id=population_id).get()[0]

            genome = pickle.loads(result['genome'])
            fitness = pickle.loads(result['fitness'])
            population = pop.Population(
                population_id=result['id'],
                experiment_id=result['experiment_id'],
                generation_number=result['generation_number'],
                genome=genome,
                fitness=fitness
            )
            return population
        except HostNotFoundException:
            raise

    def find_max_fitness(self, experiment_id):
        try:
            results = self._reader(
                table=self.POPULATIONS_TABLE
            ).where(['experiment_id', '=', experiment_id]).get()
            # 最後の記録のpopulationのfitnessを取り出す
            fitness = pickle.loads(results[-1]['fitness'])
            # 一番最初のエリートの適応度を最大とする(実際には違う場合もある)
            return fitness[0]
        except HostNotFoundException:
            raise
