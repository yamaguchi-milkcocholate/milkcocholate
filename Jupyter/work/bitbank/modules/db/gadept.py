from modules.db import writer


class GeneticAlgorithmsDepartment:

    def __init__(self, host):
        self._table = 'genetic_algorithms'
        self._columns = [
            'id',
            'name',
            'spec',
        ]
        self._writer = writer.Writer(host)

    def give_writer_task(self, columns, values):
        self._writer.write(self._table, columns, values)
