from modules.db import writer


class PopulationsDepartment:

    def __init__(self, host):
        self._table = 'populations'
        self._columns = [
            'experiment_id',
            'generation_number',
            'genome',
            'fitness',
        ]
        self._writer = writer.Writer(host=host)

    def give_writer_task(self, values):
        """
        Writerクラスを使って、データベースに複数行を挿入
        :param values: array 各要素は一行分書き込むデータの配列
        """
        self._writer.connect()
        self._writer.write_with_auto_increment_id(self._table, self._columns, values)
