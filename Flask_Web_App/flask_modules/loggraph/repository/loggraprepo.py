from flask_modules.db import reader
from flask_modules.loggraph import loggraph


class LogGraphRepository:
    EXPERIMENT_LOGS_TABLE = 'experiment_logs'

    def __init__(self, host):
        self._reader = reader.Reader(host=host)

    def get_log_graph(self, population_id):
        result = self._reader(
            table=self.EXPERIMENT_LOGS_TABLE
        ).select().where(['population_id', '=', population_id]).get()
            log_graph = loggraph.LogGraph(population_id=population_id, plot_data=result)
            return log_graph
