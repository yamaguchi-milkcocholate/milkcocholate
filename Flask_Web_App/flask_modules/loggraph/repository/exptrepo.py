import pickle
from flask_modules.loggraph import expt
from flask_modules.loggraph.repository import repository
from flask_modules.exceptions.dbhost import HostNotFoundException


class ExperimentRepository(repository.Repository):
    EXPERIMENTS_TABLE = 'experiments'
    CROSSOVERS_TABLE = 'crossovers'
    FITNESS_FUNCTIONS_TABLE = 'fitness_functions'

    def __init__(self, host):
        try:
            super().__init__(host=host)
        except HostNotFoundException:
            raise

    def get_experiments(self):
        try:
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
                if item['hyper_parameter']:
                    hyper_params = pickle.loads(item['hyper_parameter'])
                else:
                    hyper_params = None

                experiment = expt.Experiment(
                    experiment_id=item['id'],
                    coin=item['coin'],
                    crossover_name=crossover_name,
                    fitness_function_name=fitness_function_name,
                    situation=situation,
                    hyper_params=hyper_params,
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
        except HostNotFoundException:
            raise

    def get_experiment(self, experiment_id):
        try:
            result = self._reader(
                table=self.EXPERIMENTS_TABLE
            ).find(search_id=experiment_id).get()[0]

            crossover = self._reader(
                table=self.CROSSOVERS_TABLE
            ).select().find(search_id=result['crossover_id']).get()
            crossover_name = crossover[0]['name']

            fitness_function = self._reader(
                table=self.FITNESS_FUNCTIONS_TABLE
            ).select().find(search_id=result['fitness_function_id']).get()
            fitness_function_name = fitness_function[0]['name']

            situation = pickle.loads(result['situation'])
            if result['hyper_parameter']:
                hyper_params = pickle.loads(result['hyper_parameter'])
            else:
                hyper_params = None
            return_expt = expt.Experiment(
                experiment_id=result['id'],
                coin=result['coin'],
                crossover_name=crossover_name,
                fitness_function_name=fitness_function_name,
                situation=situation,
                hyper_params=hyper_params,
                mutation_rate=result['mutation_rate'],
                cross_rate=result['cross_rate'],
                population=result['population'],
                elite_num=result['elite_num'],
                start_time=result['start_at'],
                end_time=result['end_at'],
                execute_time=result['execute_time']
            )
            return return_expt
        except HostNotFoundException:
            raise

    def get_bollingerband(self):
        try:
            bollinger_band = 2
            bollinger_band_results = self._reader(
                table=self.EXPERIMENTS_TABLE
            ).where(['fitness_function_id', '=', bollinger_band]).get()
            bollinger_band_period_goal = 3
            bollinger_band_period_goal_results = self._reader(
                table=self.EXPERIMENTS_TABLE
            ).where(['fitness_function_id', '=', bollinger_band_period_goal]).get()
            results = bollinger_band_results
            if len(results) is 0:
                results = bollinger_band_period_goal_results
            else:
                results = results + bollinger_band_period_goal_results
            return_expt = list()
            for i in range(len(results)):
                hyper_params = pickle.loads(results[i]['hyper_parameter'])
                situation = pickle.loads(results[i]['situation'])
                crossover = self._reader(
                    table=self.CROSSOVERS_TABLE
                ).select().find(search_id=results[i]['crossover_id']).get()
                crossover_name = crossover[0]['name']

                fitness_function = self._reader(
                    table=self.FITNESS_FUNCTIONS_TABLE
                ).select().find(search_id=results[i]['fitness_function_id']).get()
                fitness_function_name = fitness_function[0]['name']
                return_expt.append(expt.Experiment(
                    experiment_id=results[i]['id'],
                    coin=results[i]['coin'],
                    crossover_name=crossover_name,
                    fitness_function_name=fitness_function_name,
                    situation=situation,
                    hyper_params=hyper_params,
                    mutation_rate=results[i]['mutation_rate'],
                    cross_rate=results[i]['cross_rate'],
                    population=results[i]['population'],
                    elite_num=results[i]['elite_num'],
                    start_time=results[i]['start_at'],
                    end_time=results[i]['end_at'],
                    execute_time=results[i]['execute_time']
                ))
            return return_expt
        except HostNotFoundException:
            raise

    def get_bollingerband_ti(self):
        try:
            bollingerband_ti = 4
            bollingerband_ti_results = self._reader(
                table=self.EXPERIMENTS_TABLE
            ).where(['fitness_function_id', '=', bollingerband_ti]).get()
            results = bollingerband_ti_results

            return_expt = list()
            for i in range(len(results)):
                hyper_params = pickle.loads(results[i]['hyper_parameter'])
                situation = pickle.loads(results[i]['situation'])
                crossover = self._reader(
                    table=self.CROSSOVERS_TABLE
                ).select().find(search_id=results[i]['crossover_id']).get()
                crossover_name = crossover[0]['name']

                fitness_function = self._reader(
                    table=self.FITNESS_FUNCTIONS_TABLE
                ).select().find(search_id=results[i]['fitness_function_id']).get()
                fitness_function_name = fitness_function[0]['name']
                return_expt.append(expt.Experiment(
                    experiment_id=results[i]['id'],
                    coin=results[i]['coin'],
                    crossover_name=crossover_name,
                    fitness_function_name=fitness_function_name,
                    situation=situation,
                    hyper_params=hyper_params,
                    mutation_rate=results[i]['mutation_rate'],
                    cross_rate=results[i]['cross_rate'],
                    population=results[i]['population'],
                    elite_num=results[i]['elite_num'],
                    start_time=results[i]['start_at'],
                    end_time=results[i]['end_at'],
                    execute_time=results[i]['execute_time']
                ))
            return return_expt
        except HostNotFoundException:
            raise
