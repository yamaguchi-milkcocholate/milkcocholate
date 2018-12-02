import pymysql.cursors
import pickle
from pytz import timezone
from datetime import datetime
from bitbank.exceptions.schedcancel import SchedulerCancelException
from bitbank.apigateway import ApiGateway
from bitbank.order import Order


class Bot:
    BUY = 1
    STAY = 2
    SELL = 3

    USER = 'milkcocholate'
    PASSWORD = 'milkchocolate22'
    DB = 'milkcocholate'
    CHARSET = 'utf8'

    DEFAULT_TYPE = 'market'

    def __init__(self, host, population_id, genome_id, adviser, pair, api_key, api_secret):
        """
        :param host:          string          データベースのホスト
        :param population_id: integer         テーブル populationsのid. 遺伝子群を特定
        :param genome_id:     integer         遺伝子群のNo.を特定
        :param adviser:       bitbank.adviser テクニカル分析結果から売却の指示をするクラスのインスタンス
        :param pair:          string          通貨のペア
        :param api_key:       string          APIキー
        :param api_secret     string          APIシークレットキー
        """
        self.__host = host
        self.__adviser = adviser
        self.__pair = pair
        self.__coin = pair.slice('_')[0]
        self.__yen = pair.slice('_')[1]
        self.__api_gateway = ApiGateway(api_key=api_key, api_secret=api_secret)
        self.order_ids = list()
        self.genome = None
        self.__load_genome(population_id=population_id, genome_id=genome_id)

    def __call__(self):
        # 注文の情報を確認
        orders = self.fetch_orders()

        # 注文があった場合
        if orders is not False:
            # 約定していない注文をキャンセル(その後リストから削除)。成立していればリストから削除
            for order in orders:
                # 約定注文
                if order['status'] == 'FULLY_FILLED':
                    # DBへ書き込む
                    self.__insert_filled_order(
                        order_id=order['order_id'],
                        average_price=order['average_price'],
                        filled_at=self.__now()
                    )
                    # リストから削除
                    self.order_ids.remove(order['order_id'])
                # 注文中
                else:
                    # DBへ書き込む
                    self.__insert_canceled_order(
                        order_id=order['order_id'],
                        average_price=order['average_price'],
                        remaining_amount=order['remaining_amount'],
                        executed_amount=order['executed_amount'],
                        status=order['status'],
                        canceled_at=self.__now()
                    )
                    self.order_ids.remove(order['order_id'])
        # アセットを読み込む
        assets_free_amount = self.fetch_asset()
        print(self.__now() + '   ', end='')
        for key in assets_free_amount:
            print(key + ': ' + assets_free_amount[key] + '    ', end='')
        print()

        # 日本円があるとき、新規注文する
        if assets_free_amount[self.__yen] > 0:
            operation, price = self.__adviser.operation(
                genome=self.genome,
                has_coin=False
            )
            # STAYではないとき
            if operation is not self.STAY:
                # 新規注文
                result = self.new_orders(
                    price=price,
                    amount=assets_free_amount[self.__yen],
                    side=self.__operation_to_side(operation=operation),
                    order_type=self.DEFAULT_TYPE
                )
                # DBへ書き込み
                self.__insert_order(
                    order_id=result.order_id,
                    pair=result.pair,
                    side=result.side,
                    type=result.type,
                    price=result.price,
                    amount=result.start_amount,
                    ordered_at=result.ordered_at
                )
                self.order_ids.append(result.order_id)
                print(result.ordered_at + '   ' + self.__operation_to_side(operation=operation)
                      + ' ' + result.start_amount + ' ' + result.price)
            else:
                print(self.__now() + '   ' + 'stay')

        # コインがあるとき、新規注文する
        if assets_free_amount[self.__coin] > 0:
            operation, price = self.__adviser.operation(
                genome=self.genome,
                has_coin=True
            )
            # STAYではないとき
            if operation is not self.STAY:
                # 新規注文
                result = self.new_orders(
                    price=price,
                    amount=assets_free_amount[self.__coin],
                    side=self.__operation_to_side(operation=operation),
                    order_type=self.DEFAULT_TYPE
                )

                # DBへ書き込み
                self.__insert_order(
                    order_id=result.order_id,
                    pair=result.pair,
                    side=result.side,
                    type=result.type,
                    price=result.price,
                    amount=result.start_amount,
                    ordered_at=result.ordered_at
                )
                self.order_ids.append(result.order_id)
                print(result.ordered_at + '   ' + self.__operation_to_side(operation=operation)
                      + ' ' + result.start_amount + ' ' + result.price)
            else:
                print(self.__now() + '   ' + 'stay')

    def __operation_to_side(self, operation):
        if operation is self.BUY:
            return 'buy'
        elif operation is self.SELL:
            return 'sell'

    def __load_genome(self, population_id, genome_id):
        """
        データベースのレコードから遺伝子をセットする
        :param population_id:
        :param genome_id:
        """
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
            raise SchedulerCancelException('Fail to load genome')
        sql = "SELECT `genome` FROM `populations` WHERE `id` = %s;"
        placeholder = [population_id]
        with connection.cursor() as cursor:
            cursor.execute(sql, placeholder)
            self.genome = pickle.loads(cursor.fetchall()[0]['genome'])[genome_id]

    def fetch_asset(self):
        """
        アセットの利用可能な量を読み込む
        :return: dict 利用可能な量
        """
        results = self.__api_gateway.use_asset()
        assets = dict()
        for result in results:
            if result['asset'] == self.__coin:
                assets[self.__coin] = result['free_amount']
            elif result['asset'] == self.__yen:
                assets[self.__yen] = result['free_amount']
        return assets

    def new_orders(self, price, amount, side, order_type):
        """
        新規注文を行う
        :param price:      number
        :param amount:     number
        :param side:       string
        :param order_type: string
        :return: bitbank.order.Order 注文情報
        """
        result = self.__api_gateway.new_order(
            pair=self.__pair,
            price=price,
            amount=amount,
            side=side,
            order_type=order_type
        )
        if result['order_id'] is None:
            raise SchedulerCancelException('Fail to order')

        # DBへ書き込む
        self.__insert_order(
            order_id=result['order_id'],
            pair=result['pair'],
            side=result['side'],
            type=result['type'],
            price=result['price'],
            amount=result['start_amount'],
            ordered_at=result['ordered_at']
        )

        order = Order(
            order_id=result['order_id'],
            pair=result['pair'],
            side=result['side'],
            type=result['type'],
            price=result['price'],
            start_amount=result['start_amount'],
            remaining_amount=result['remaining_amount'],
            executed_amount=result['executed_amount'],
            average_price=result['average_price'],
            ordered_at=result['ordered_at'],
            status=result['status']
        )
        return order

    def cancel_orders(self, order_id):
        """
        現在の注文をキャンセルする
        :param order_id:  number
        """
        result = self.__api_gateway.cancel_order(
            pair=self.__pair,
            order_id=order_id
        )
        if result['order_id'] == order_id:
            raise SchedulerCancelException('Fail to cancel order')

        # DBへ書き込む
        self.__insert_canceled_order(
            order_id=result['order_id'],
            average_price=result['average_price'],
            remaining_amount=result['remaining_amount'],
            executed_amount=result['executed_amount'],
            status=result['status'],
            canceled_at=self.__now()
        )

    def fetch_orders(self):
        """
        現在の注文の状況を確認する
        :return: False | list  注文が存在すればその情報、なければFalse
        {
            'order_id_1': bitbank.order.Order,
            'order_id_2': bitbank.order.Order,
        }
        """
        if len(self.order_ids) is 0:
            return False
        results = self.__api_gateway.use_orders_info(
            pair=self.__pair,
            order_ids=self.order_ids
        )
        if results['orders'] is None:
            raise SchedulerCancelException('Fail to get orders information')

        orders = dict()
        for result in results['orders']:
            order = Order(
                order_id=result['order_id'],
                pair=result['pair'],
                side=result['side'],
                type=result['type'],
                price=result['price'],
                start_amount=result['start_amount'],
                remaining_amount=result['remaining_amount'],
                executed_amount=result['executed_amount'],
                average_price=result['average_price'],
                ordered_at=result['ordered_at'],
                status=result['status']
            )
            orders[result['order_id']] = order
            # 注文が約定されればDBへ書き込む
            if result['status'] == 'FULLY_FILLED':
                self.__insert_filled_order(
                    order_id=result['order_id'],
                    average_price=result['average_price'],
                    filled_at=self.__now()
                )
        return orders

    def __insert_order(self, order_id, pair, side, type, price, amount, ordered_at):
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
            raise SchedulerCancelException('Fail to insert order in connecting DB')
        sql = "INSERT INTO `orders` " \
              "(`order_id`, `pair`, `side`, `type`, `price`, `amount`, `ordered_at`) " \
              "VALUES (%s, %s, %s, %s, %s, %s, %s);"
        placeholder = [
            order_id,
            pair,
            side,
            type,
            price,
            amount,
            ordered_at
        ]
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, placeholder)
        except Exception:
            connection.rollback()
            connection.close()
            raise SchedulerCancelException('Fail to insert order in inserting DB')
        finally:
            connection.commit()
            connection.close()

    def __insert_filled_order(self, order_id, average_price, filled_at):
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
            raise SchedulerCancelException('Fail to insert filled order in connecting DB')
        sql = "INSERT INTO `filled_orders` " \
              "(`order_id`, `average_price`,  `filled_at`) " \
              "VALUES (%s, %s, %s);"
        placeholder = [
            order_id,
            average_price,
            filled_at
        ]
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, placeholder)
        except Exception:
            connection.rollback()
            connection.close()
            raise SchedulerCancelException('Fail to insert filled order in inserting DB')
        finally:
            connection.commit()
            connection.close()

    def __insert_canceled_order(self, order_id, average_price,
                                remaining_amount, executed_amount, status, canceled_at):
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
            raise SchedulerCancelException('Fail to insert canceled order in connecting DB')
        sql = "INSERT INTO `canceled_orders` " \
              "(`order_id`, `average_price`,  `remaining_amount`, `executed_amount`, `status`, `canceled_at`) " \
              "VALUES (%s, %s, %s, %s, %s, %s);"
        placeholder = [
            order_id,
            average_price,
            remaining_amount,
            executed_amount,
            status,
            canceled_at
        ]
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, placeholder)
        except Exception:
            connection.rollback()
            connection.close()
            raise SchedulerCancelException('Fail to insert canceled order in inserting DB')
        finally:
            connection.commit()
            connection.close()

    @staticmethod
    def __now():
        return datetime.now(timezone('UTC')).astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H%M%S')

