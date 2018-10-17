from modules.db import department


class GeneticAlgorithmsDepartment(department.Department):

    def __init__(self, host):
        super().__init__(host=host)
        self._table = 'genetic_algorithms'
        self._columns = [
            'name',
            'spec',
        ]

    def give_writer_task(self, values):
        """
        Writerクラスを使って、データベースに複数行を挿入
        :param values: array 各要素は一行分書き込むデータの配列
        """
        super().give_writer_task(values=values)

    def make_writer_find_next_id(self):
        """
        Writerクラスを使って、次のAuto_increment_idを取り出す
        :return: auto_increment_id int  次のAuto_increment_id
        """
        return super().make_writer_find_next_id()
