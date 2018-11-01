from flask_modules.loggraph import loggraph
from flask_modules.loggraph.repository import repository


class LogGraphRepository(repository.Repository):
    EXPERIMENT_LOGS_TABLE = 'experiment_logs'

    def __init__(self, host):
        super().__init__(host=host)

    def get_log_graph(self, population_id):
        result = self._reader(
            table=self.EXPERIMENT_LOGS_TABLE
        ).select().where(['population_id', '=', population_id]).get()
            log_graph = loggraph.LogGraph(population_id=population_id, plot_data=result)
            return log_graph
