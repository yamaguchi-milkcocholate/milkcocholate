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
        """
        Writerクラスを使って、データベースに複数行を挿入
        :param values: array 各要素は一行分書き込むデータの配列
        """
        self._writer.connect()
        self._writer.write_with_auto_increment_id(self._table, self._columns, values)
