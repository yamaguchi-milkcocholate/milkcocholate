import python_bitbankcc
import pymysql.cursors
import pickle
from bitbank.exceptions.schedcancel import SchedulerCancelException
from bitbank.security import Security


class Bot:
    BUY = 1
    STAY = 2
    SELL = 3

    USER = 'milkcocholate'
    PASSWORD = 'milkchocolate22'
    DB = 'milkcocholate'
    CHARSET = 'utf8'

    def __init__(self, host, population_id, genome_id):
        self.__security = Security()
        self.__host = host
        self.genome = None
        self.__yen_position = None
        self.__coin_position = None
        self.__load_genome(population_id=population_id, genome_id=genome_id)

    def processing(self):
        pass

    def __load_genome(self, population_id, genome_id):
        try:
            connection = pymysql.connect(
                host=self.__host,
                user=self.USER,
                db=self.DB,
                password=self.PASSWORD,
                charset=self.CHARSET,
                cursorclass=pymysql.cursors.DictCursor
            )
        except pymysql.err.OperationalError:
            raise
        sql = "SELECT `genome` FROM `populations` WHERE `id` = %s;"
        placeholder = [population_id]
        with connection.cursor() as cursor:
            cursor.execute(sql, placeholder)
            self.genome = pickle.loads(cursor.fetchall()[0]['genome'])[genome_id]
