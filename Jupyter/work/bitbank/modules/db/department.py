from abc import ABC
from modules.db import writer


class Department(ABC):

    def __init__(self, host):
        self._writer = writer.Writer(host=host)
        self._table = None
        self._columns = None

    def give_writer_task(self, values):
        """
        Writerクラスを使って、データベースに複数行を挿入
        :param values: array 各要素は一行分書き込むデータの配列
        """
        self._writer.connect()
        self._writer.write_with_auto_increment_id(self._table, self._columns, values)

    def make_writer_find_next_id(self):
        """
        Writerクラスを使って、次のAuto_increment_idを取り出す
        :return: auto_increment_id int  次のAuto_increment_id
        """
        self._writer.connect()
        auto_increment_id = self._writer.next_auto_increment_id(self._table)
        return auto_increment_id
