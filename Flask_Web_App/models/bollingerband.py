from flask_modules.loggraph.repository import exptrepo
from flask_modules.loggraph.repository import poprepo
from flask_modules.exceptions.dbhost import HostNotFoundException


class BollingerBandController:

    def __init__(self, host):
        self.__host = host

    def __call__(self):
        """
        :return:
        [
            {'experiment: Experiment, max_fitness: int},
            {'experiment: Experiment, max_fitness: int},
        ]
        """
        try:
            pop_repository = poprepo.PopulationRepository(host=self.__host)
            expt_repository = exptrepo.ExperimentRepository(host=self.__host)
            experiments = expt_repository.get_bollinger_band()
            bollingerbands = list()
            for i in range(len(experiments)):
                el = dict()
                el['experiment'] = experiments[i]
                result = pop_repository.find_max_fitness_and_genome(experiment_id=experiments[i].id)
                el['max_fitness'] = result['fitness']
                el['max_genome'] = result['genome']
                bollingerbands.append(el)
            return bollingerbands
        except HostNotFoundException:
            raise
