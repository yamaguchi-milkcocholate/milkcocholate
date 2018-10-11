from modules.db import writer


class ExperimentLogsDepartment:

    def __init__(self, host):
        self._table = 'experiment_logs'
        self._columns = [
            'id',
            'experiment_id',
            'position',
            'price',
            'logged_at'
        ]
        self._writer = writer.Writer(host)

    def give_writer_task(self, columns, values):
        self._writer.write(self._table, columns, values)
