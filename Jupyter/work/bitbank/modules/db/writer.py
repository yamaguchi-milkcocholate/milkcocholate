import pymysql.cursors


class Writer:
    USER = ''
    PASSWORD = ''
    DB = ''
    CHARSET = ''

    def __init__(self, host):
        self._connection = pymysql.connect(
            host=host,
            user=self.USER,
            db=self.DB,
            password=self.PASSWORD,
            charset=self.CHARSET
        )

    def write(self, table, columns, value):
        """
        一行を書き込む
        :param table:   string  テーブル名
        :param columns: array   カラム
        :param value:   array   カラムに書き込む値
        """
        columns_str, value_str = self._make_placeholder_str(columns)
        with self._connection.cursor() as cursor:
            sql = "INSERT INTO '" + table + "' " + columns_str + " VALUES " + value_str
            cursor.execute(sql, value)
            self._connection.commit()

    @staticmethod
    def _make_placeholder_str(columns):
        column_str = "('" + columns[0]
        value_str = "(%s"
        array_len = len(columns)
        if array_len is 1:
            return column_str + "')", value_str + ")"
        else:
            for i in range(1, array_len):
                column_str = column_str + "', '" + columns[i]
                value_str = value_str + ", %s"
            return column_str + "')", value_str + ")"

    def begin_transaction(self):
        self._connection.begin()

    def rollback(self):
        self._connection.rollback()
