from modules.db import writer


class FitnessFunctionsDepartment:

    def __init__(self, host):
        self._table = 'fitness_functions'
        self._columns = [
            'name',
            'spec',
        ]
        self._writer = writer.Writer(host)

    def give_writer_task(self, values):
        self._writer.connect()
        self._writer.write_with_auto_increment_id(self._table, self._columns, values)