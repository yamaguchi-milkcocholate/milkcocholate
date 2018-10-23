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
        plot_data = dict()
        plot_data['time'] = list()
        plot_data['position'] = list()
        plot_data['price'] = list()
        str_format = '%Y-%m-%d %H:%M:%S'
        for item in result:
            plot_data['time'].append(item['logged_at'].strftime(str_format))
            plot_data['position'].append(item['position'])
            plot_data['price'].append(item['price'])
        log_graph = loggraph.LogGraph(population_id=population_id, plot_data=plot_data)
        return log_graph
