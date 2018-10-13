from modules.db import writer


class ExperimentLogsDepartment:

    def __init__(self, host):
        self._table = 'experiment_logs'
        self._columns = [
            'experiment_id',
            'position',
            'price',
            'logged_at'
        ]
        self._writer = writer.Writer(host)

    def give_writer_task(self, values):
        self._writer.connect()
        self._writer.write_with_auto_increment_id(self._table, self._columns, values)
