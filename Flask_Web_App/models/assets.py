import pymysql.cursors
import numpy as np
import matplotlib.pyplot as plt


class AssetsCollector:

    def __init__(self, host):
        self.__host = host

    def connect(self):
        """
        DBに接続
        :return: pymysql.connect コネクション
        """
        try:
            connection = pymysql.connect(
                host=self.__host,
                user='milkcocholate',
                db='milkcocholate',
                password='milkchocolate22',
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.err.OperationalError:
            raise
        return connection

    def show_plot(self, start, end, coin):
        connection = self.connect()
        sql = "SELECT * FROM  `assets` WHERE " \
              "`coin` = %s AND %s <= `time` AND `time` <= %s " \
              "ORDER BY `time` DESC;"
        placeholder = [coin, start, end]

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, placeholder)
                jpy = cursor.fetchall()
        except Exception:
            connection.close()
            raise
        finally:
            connection.close()

        x, y = self.__axis_array(data=jpy, x_title='time', y_title='price')

        plt.title('assets')
        plt.xlabel('time')
        plt.ylabel('price')
        plt.plot(x, y)
        plt.show()

    @staticmethod
    def __axis_array(data, x_title, y_title):
        """
        :param data:     dict[]
        :param x_title:  string
        :param y_title:  string
        :return: numpy, numpy
        """
        x_list = list()
        y_list = list()
        for line in data:
            x_list.append(line[x_title])
            y_list.append(line[y_title])
        return np.asarray(x_list), np.asarray(y_list)
