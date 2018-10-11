from modules.db import writer


class FitnessFunctionsDepartment:

    def __init__(self, host):
        self._table = 'fitness_functions'
        self._columns = [
            'id',
            'name',
            'spec',
        ]
        self._writer = writer.Writer(host)

    def give_writer_task(self, columns, values):
        self._writer.write(self._table, columns, values)
