from modules.db import writer


class ExperimentsDepartment:

    def __init__(self, host):
        self._table = 'experiments'
        self._columns = [
            'genetic_algorithm_id',
            'fitness_function_id',
            'situation',
            'mutation_rate',
            'cross_rate',
            'population',
            'elite_num',
            'start_at',
            'end_at',
            'execute_time',
        ]
        self._writer = writer.Writer(host)

    def give_writer_task(self, values):
        self._writer.connect()
        self._writer.write_with_auto_increment_id(self._table, self._columns, values)
