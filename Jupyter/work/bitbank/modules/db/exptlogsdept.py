from modules.db import writer


class ExperimentLogsDepartment:

    def __init__(self, host):
        self._table = 'experiment_logs'
        self._columns = [
            'population_id',
            'position',
            'price',
            'logged_at'
        ]
        self._writer = writer.Writer(host)

    def give_writer_task(self, values):
        """
        Writerクラスを使って、データベースに複数行を挿入
        :param values: array 各要素は一行分書き込むデータの配列
        """
        self._writer.connect()
        self._writer.write_with_auto_increment_id(self._table, self._columns, values)
