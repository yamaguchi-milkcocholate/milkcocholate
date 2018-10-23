import pymysql.cursors


class Reader:
    USER = 'milkcocholate'
    PASSWORD = 'milkchocolate22'
    DB = 'milkcocholate'
    CHARSET = 'utf8'

    def __init__(self, host):
        self._host = host
        self._connection = None
        self._sql = None
        self._table = None
        self._selects = list()
        self._wheres = list()

    def __call__(self, table):
        self._table = table
        return self

    def _connect(self):
        """
        データベースに接続
        """
        self._connection = pymysql.connect(
            host=self._host,
            user=self.USER,
            db=self.DB,
            password=self.PASSWORD,
            charset=self.CHARSET,
            cursorclass=pymysql.cursors.DictCursor
        )

    def get_sql(self):
        return self._sql

    def get_placeholder(self):
        placeholder = dict()
        placeholder['table'] = self._table
        placeholder['selects'] = self._selects
        placeholder['wheres'] = self._wheres
        return placeholder

    def select(self, *args):
        self._selects.extend(args)
        return self

    def find(self, search_id):
        self._wheres.append(['id', '=', search_id])
        return self

    def where(self, *args):
        self._wheres.extend(args)
        return self

    def get(self, should_execute=True):
        table = self._table
        selects = self._selects
        wheres = self._wheres
        self._table = None
        self._selects = list()
        self._wheres = list()

        placeholder = list()
        self._sql = "SELECT "
        if not selects:
            self._sql = self._sql + "* "
        else:
            for select_i in range(len(selects)):
                if select_i is len(selects) - 1:
                    self._sql = self._sql + "`" + selects[select_i] + "` "
                else:
                    self._sql = self._sql + "`" + selects[select_i] + "` "

        if not table:
            self._sql = None
            raise TypeError('table is empty')
        self._sql = self._sql + "FROM `" + table + "` "

        if wheres:
            self._sql = self._sql + "WHERE "
        for where_i in range(len(wheres)):
            placeholder.append(wheres[where_i][2])
            if where_i is len(wheres) - 1:
                self._sql = self._sql + "`" + wheres[where_i][0] + "` " + wheres[where_i][1] + " %s "
            else:
                self._sql = self._sql + "`" + wheres[where_i][0] + "` " + wheres[where_i][1] + " %s and "
        if should_execute:
            return self.execute_query(sql=self._sql, placeholder=placeholder)

    def execute_query(self, sql, placeholder):
        self._connect()
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(sql, placeholder)
                result = cursor.fetchone()
        except Exception:
            self._connection.close()
            raise
        finally:
            self._connection.close()
        return result
