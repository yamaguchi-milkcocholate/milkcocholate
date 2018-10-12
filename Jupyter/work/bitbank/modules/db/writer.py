import pymysql.cursors


class Writer:
    USER = 'milkcocholate'
    PASSWORD = 'milkchocolate22'
    DB = 'milkcocholate'
    CHARSET = 'utf8mb4'

    def __init__(self, host):
        self._connection = pymysql.connect(
            host=host,
            user=self.USER,
            db=self.DB,
            password=self.PASSWORD,
            charset=self.CHARSET
        )

    def write(self, table, columns, values):
        """
        一行を書き込む
        :param table:   string  テーブル名
        :param columns: array   カラム
        :param values:   array   カラムに書き込む値
        """
        columns, values = self._auto_increment_id_check(columns, values)
        columns_str, value_str = self._make_placeholder_str(columns)
        with self._connection.cursor() as cursor:
            sql = "INSERT INTO `" + table + "` " + columns_str + " VALUES " + value_str + ';'
            cursor.execute(sql, values)
            self._connection.commit()

    @staticmethod
    def _make_placeholder_str(columns):
        column_str = "(`" + columns[0]
        value_str = "(%s"
        array_len = len(columns)
        if array_len is 1:
            return column_str + "`)", value_str + ")"
        else:
            for i in range(1, array_len):
                column_str = column_str + "`, `" + columns[i]
                value_str = value_str + ", %s"
            return column_str + "`)", value_str + ")"

    def begin_transaction(self):
        self._connection.begin()

    def rollback(self):
        self._connection.rollback()

    def get_connection(self):
        return self._connection

    @staticmethod
    def _auto_increment_id_check(columns, values):
        if 'id' in columns:
            # id指定されているとき
            if len(columns) is len(values):
                return columns, values
            # 誤ってidをcolumnに追加したとする
            elif len(columns) is (len(values) + 1):
                columns.remove('id')
                return columns, values
            else:
                raise TypeError('list length is not match...')
        else:
            # id指定せずにauto_incrementを利用するとき
            if len(columns) is len(values):
                return columns, values
            # 誤ってidの値を入れてしまったとする
            elif (len(columns) + 1) is len(values):
                values.pop(0)
                return columns, values
            else:
                raise TypeError('list length is not math...')


