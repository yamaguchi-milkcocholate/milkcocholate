import pickle
from flask_modules.loggraph import expt
from flask_modules.loggraph.repository import repository


class ExperimentRepository(repository.Repository):
    EXPERIMENTS_TABLE = 'experiments'
    CROSSOVERS_TABLE = 'crossovers'
    FITNESS_FUNCTIONS_TABLE = 'fitness_functions'

    def __init__(self, host):
        self._reader = reader.Reader(host=host)

    def get_experiments(self):
        result = self._reader(
            table=self.EXPERIMENTS_TABLE
        ).select().get()
        experiment_list = list()
        for item in result:
            crossover = self._reader(
                table=self.CROSSOVERS_TABLE
            ).select().find(search_id=item['crossover_id']).get()
            crossover_name = crossover[0]['name']

            fitness_function = self._reader(
                table=self.FITNESS_FUNCTIONS_TABLE
            ).select().find(search_id=item['fitness_function_id']).get()
            fitness_function_name = fitness_function[0]['name']

            situation = pickle.loads(item['situation'])

            experiment = expt.Experiment(
                experiment_id=item['id'],
                crossover_name=crossover_name,
                fitness_function_name=fitness_function_name,
                situation=situation,
                mutation_rate=item['mutation_rate'],
                cross_rate=item['cross_rate'],
                population=item['population'],
                elite_num=item['elite_num'],
                start_time=item['start_at'],
                end_time=item['end_at'],
                execute_time=item['execute_time']
            )
            experiment_list.append(experiment)
        return experiment_list
