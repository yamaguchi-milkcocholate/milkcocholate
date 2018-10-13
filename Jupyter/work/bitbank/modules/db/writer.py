import pymysql.cursors


class Writer:
    USER = 'milkcocholate'
    PASSWORD = 'milkchocolate22'
    DB = 'milkcocholate'
    CHARSET = 'utf8'

    def __init__(self, host):
        self._host = host
        self._connection = None

    def connect(self):
        self._connection = pymysql.connect(
            host=self._host,
            user=self.USER,
            db=self.DB,
            password=self.PASSWORD,
            charset=self.CHARSET
        )

    def write_with_auto_increment_id(self, table, columns, chunk):
        """
        複数行をauto_incrementで書き込む
        :param table:     string  テーブル名
        :param columns:   array   テーブルのカラム
        :param chunk:     array   挿入する複数行の値
        """
        column_str, value_str = self._make_chunk_placeholder_str_with_auto_increment_id(columns, chunk)
        try:
            with self._connection.cursor() as cursor:
                sql = "INSERT INTO `" + table + "` " + column_str + " VALUES " + value_str + ";"
                cursor.execute(sql, sum(chunk, []))
        except Exception:
            self._connection.rollback()
            self._connection.close()
            raise
        finally:
            self._connection.commit()
            self._connection.close()

    def get_connection(self):
        return self._connection

    def get_host(self):
        return self._host

    def set_host(self, host):
        self._host = host

    def _make_chunk_placeholder_str_with_auto_increment_id(self, columns, chunk):
        """
        auto_incrementで複数行を挿入するsql文に使う文字列を生成
        :param columns: string    挿入するテーブルのカラム
        :param chunk:   array     挿入する複数行の値
        :return: string, string:  COLUMNS部分, VALUES部分
        """
        if 'id' in columns:
            raise TypeError('auto_increment mode has no "id"...')
        column_str, value_str = self._make_placeholder_str(columns)
        for chunk_i in range(len(chunk) - 1):
            value_str = value_str + ', ' + value_str
        return column_str, value_str

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
