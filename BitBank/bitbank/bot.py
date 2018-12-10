import pymysql.cursors
import pickle
import time
from pytz import timezone
from datetime import datetime
from bitbank.exceptions.schedcancel import SchedulerCancelException
from bitbank.apigateway import ApiGateway
from bitbank.order import Order
from bitbank.line import Line


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
        self.__coin = pair.split('_')[0]
        self.__yen = pair.split('_')[1]
        self.__api_gateway = ApiGateway(api_key=api_key, api_secret=api_secret)
        self.order_ids = list()
        self.genome = None
        self.__load_genome(population_id=population_id, genome_id=genome_id)
        self.__line = Line()

    def __call__(self):
        # 注文の情報を確認
        orders = self.fetch_orders()

        # 注文があった場合
        if orders is not False:
            # 約定していない注文をキャンセル(その後リストから削除)。成立していればリストから削除
            for order_id in orders:
                # 約定注文
                if orders[order_id].status == 'FULLY_FILLED':
                    # DBへ書き込む
                    self.__insert_filled_order(
                        order_id=orders[order_id].order_id,
                        average_price=orders[order_id].average_price,
                        filled_at=self.__now()
                    )
                    # リストから削除
                    self.order_ids.remove(orders[order_id].order_id)
                # 注文中
                else:
                    # DBへ書き込む
                    self.__insert_canceled_order(
                        order_id=orders[order_id].order_id,
                        average_price=orders[order_id].average_price,
                        remaining_amount=orders[order_id].remaining_amount,
                        executed_amount=orders[order_id].executed_amount,
                        status=orders[order_id].status,
                        canceled_at=self.__now()
                    )
                    self.order_ids.remove(orders[order_id].order_id)
        # アセットを読み込む
        assets_free_amount = self.fetch_asset()
        print()
        print("When show this at " + self.__now() + ' ==================')
        for key in assets_free_amount:
            print(key + ': ' + assets_free_amount[key] + '    ', end='')
        print()
        print("--------------------------------------------------------")
        # 日本円があるとき、新規注文する
        if float(assets_free_amount[self.__yen]) > 0:
            operation, price = self.__adviser.operation(
                genome=self.genome,
                has_coin=False
            )
            # STAYではないとき
            if operation != int(self.STAY):
                # 新規注文
                result = self.new_orders(
                    price=price,
                    amount=(float(assets_free_amount[self.__yen]) / price),
                    side=self.__operation_to_side(operation=operation),
                    order_type=self.DEFAULT_TYPE
                )
                print(result.ordered_at + '   ' + self.__operation_to_side(operation=operation)
                      + ' ' + result.start_amount + ' ' + result.price)
            else:
                print(self.__now() + '   ' + 'stay')

        # コインがあるとき、新規注文する
        if float(assets_free_amount[self.__coin]) > 0:
            operation, price = self.__adviser.operation(
                genome=self.genome,
                has_coin=True
            )
            # STAYではないとき
            if operation != int(self.STAY):
                # 新規注文
                result = self.new_orders(
                    price=price,
                    amount=assets_free_amount[self.__coin],
                    side=self.__operation_to_side(operation=operation),
                    order_type=self.DEFAULT_TYPE
                )
                print(result.ordered_at + '   ' + self.__operation_to_side(operation=operation)
                      + ' ' + result.start_amount + ' ' + result.price)
            else:
                print(self.__now() + '   ' + 'stay')
        print("========================================================")

    def __operation_to_side(self, operation):
        if operation == int(self.BUY):
            return 'buy'
        elif operation == int(self.SELL):
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
        DBにアセットを書き込む(YEN, XRP)
        insert_list[''] = [
            'coin', 'amount', 'price', 'time'
        ]
        :return: dict 利用可能な量
        """
        results = self.__api_gateway.use_asset()
        assets = dict()
        insert_list = {self.__coin: [self.__coin], self.__yen: [self.__yen]}
        for result in results['assets']:
            if result['asset'] == self.__coin:
                assets[self.__coin] = result['free_amount']
                insert_list[self.__coin].append(result['onhand_amount'])
            elif result['asset'] == self.__yen:
                assets[self.__yen] = result['free_amount']
                insert_list[self.__yen].append(result['onhand_amount'])
        ticker = self.__api_gateway.use_ticker(pair=self.__pair)
        insert_list[self.__coin].append(ticker['last'])
        insert_list[self.__yen].append(ticker['last'])
        insert_list[self.__coin].append(self.__now())
        insert_list[self.__yen].append(self.__now())
        self.__insert_assets(insert_list=insert_list)
        return assets

    def new_orders(self, price, amount, side, order_type, retry=0):
        """
        新規注文を行う
        :param price:      number
        :param amount:     number
        :param side:       string
        :param order_type: string
        :param retry:      integer
        :return: bitbank.order.Order 注文情報
        """
        try:
            result = self.__api_gateway.new_order(
                pair=self.__pair,
                price=price,
                amount=amount,
                side=side,
                order_type=order_type
            )
            # Orderインスタンス化
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
            # DBへ書き込む
            self.__insert_order(
                order_id=order.order_id,
                pair=order.pair,
                side=order.side,
                type=order.type,
                price=order.price,
                amount=order.start_amount,
                ordered_at=order.ordered_at
            )
            self.new_order_message(order=order, retry=retry)
            self.order_ids.append(result['order_id'])
        except Exception as e:
            print(e)
            if '60002' in e.args[0]:
                #  60002 内容: 成行買い注文の数量上限を上回っています
                amount = float(amount) / 2.0
                order = self.new_orders(price, amount, side, order_type, retry=retry + 1)
            elif '70009' in e.args[0]:
                # 70009 ただいま成行注文を一時的に制限しています。指値注文をご利用ください
                print('60秒の遅らせて再度注文します。')
                self.__line(message='60秒の遅らせて再度注文します。')
                time.sleep(60)
                order = self.new_orders(price, amount, side, order_type, retry=retry + 1)
            else:
                self.error_message(message=e.args[0])
                raise SchedulerCancelException('Fail to order')
        return order

    def cancel_orders(self, order_id):
        """
        現在の注文をキャンセルする
        :param order_id:  number
        """
        try:
            result = self.__api_gateway.cancel_order(
                pair=self.__pair,
                order_id=order_id
            )
            self.cancel_order_message(result=result)
            self.order_ids.append(result.order_id)
        except Exception as e:
            print(e)
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
        return orders

    def __insert_assets(self, insert_list):
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
            raise SchedulerCancelException('Fail to insert assets in connecting DB')
        sql = "INSERT INTO `assets` " \
              "(`coin`, `amount`, `price`, `time`) " \
              "VALUES (%s, %s, %s, %s);"
        placeholder = insert_list[self.__coin]
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, placeholder)
        except Exception:
            connection.rollback()
            connection.close()
            raise SchedulerCancelException('Fail to insert assets in inserting DB')
        finally:
            connection.commit()
            connection.close()

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
            raise SchedulerCancelException('Fail to insert assets in connecting DB')
        placeholder = insert_list[self.__yen]
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, placeholder)
        except Exception:
            connection.rollback()
            connection.close()
            raise SchedulerCancelException('Fail to insert assets in inserting DB')
        finally:
            connection.commit()
            connection.close()

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
        except pymysql.err.OperationalError as e:
            print(e)
            print('Fail to insert order in connecting DB')
            exception = SchedulerCancelException('Fail to insert order in connecting DB')
            exception.args = ('Fail to insert order in connecting DB', )
            raise exception
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
        except Exception as e:
            print(e)
            connection.rollback()
            connection.close()
            print('Fail to insert order in inserting DB')
            exception = SchedulerCancelException('Fail to insert order in inserting DB')
            exception.args = ('Fail to insert order in inserting DB',)
            raise exception
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
        except pymysql.err.OperationalError as e:
            print(e)
            print('Fail to insert filled order in connecting DB')
            exception = SchedulerCancelException('Fail to insert filled order in connecting DB')
            exception.args = ('Fail to insert filled order in connecting DB',)
            raise exception
        sql = "INSERT INTO `filled_orders` " \
              "(`order_id`, `average_price`,  `filled_at`) " \
              "VALUES (%s, %s, %s);"
        placeholder = [
            int(order_id),
            float(average_price),
            filled_at
        ]
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, placeholder)
        except Exception as e:
            print(e)
            connection.rollback()
            connection.close()
            print('Fail to insert filled order in inserting DB')
            exception = SchedulerCancelException('Fail to insert filled order in inserting DB')
            exception.args = ('Fail to insert filled order in inserting DB',)
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
        except pymysql.err.OperationalError as e:
            print(e)
            print('Fail to insert canceled order in connecting DB')
            exception = SchedulerCancelException('Fail to insert canceled order in connecting DB')
            exception.args = ('Fail to insert canceled order in connecting DB',)
            raise exception
        sql = "INSERT INTO `canceled_orders` " \
              "(`order_id`      , `average_price`,  `remaining_amount`, `executed_amount`, `status`, `canceled_at`) " \
              "VALUES (%s, %s, %s, %s, %s, %s);"
        placeholder = [
            int(order_id),
            float(average_price),
            float(remaining_amount),
            float(executed_amount),
            status,
            canceled_at
        ]
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, placeholder)
        except Exception as e:
            print(e)
            connection.rollback()
            connection.close()
            print('Fail to insert canceled order in inserting DB')
            exception = SchedulerCancelException('Fail to insert canceled order in inserting DB')
            exception.args = ('Fail to insert canceled order in inserting DB',)
            raise SchedulerCancelException('Fail to insert canceled order in inserting DB')
        finally:
            connection.commit()
            connection.close()

    @staticmethod
    def __now():
        return datetime.now(timezone('UTC')).astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')

    def new_order_message(self, order, retry):
        side = self.__side_to_japanese(side=order.side)
        status = self.__status_to_japanese(status=order.status)
        message = "新規注文を行いました。\n" \
                  "===================\n" \
                  "" + order.pair + " " + side + "注文 " + status + "\n" \
                  "注文ID: {}\n" \
                  "時刻: {}\n" \
                  "価格: {}\n" \
                  "数量: {}\n" \
                  "再要求回数: {}\n" \
                  "===================".format(
                        order.order_id,
                        order.ordered_at,
                        order.price,
                        order.start_amount,
                        retry
                  )
        message.replace('n', '%0D%0A')
        self.__line(message=message)

    def cancel_order_message(self, result):
        side = self.__side_to_japanese(side=result['side'])
        status = self.__status_to_japanese(status=result['status'])
        message = "注文を取り消しました。\n" \
                  "===================\n" \
                  "" + result['pair'] + " " + side + "注文 " + status + "\n" \
                  "注文ID: {}\n" \
                  "時刻: {}\n" \
                  "価格: {}\n" \
                  "平均価格: {}\n" \
                  "数量: {}\n" \
                  "約定数量: {}\n" \
                  "===================".format(
                        result['order_id'],
                        self.__now(),
                        result['price'],
                        result['average_price'],
                        result['start_amount'],
                        result['executed_amount'],
                  )
        message.replace('n', '%0D%0A')
        self.__line(message=message)

    def error_message(self, message):
        message = "エラー発生!!\n" \
                  "===================\n" \
                  "" + message + "\n" \
                  "==================="
        self.__line(message=message)

    @staticmethod
    def __side_to_japanese(side):
        if side == 'buy':
            japanese = '買い'
        else:
            japanese = '売り'
        return japanese

    @staticmethod
    def __status_to_japanese(status):
        if status == 'UNFILLED':
            japanese = '注文中'
        elif status == 'PARTIALLY_FILLED':
            japanese = '注文中(一部約定)'
        elif status == 'FULLY_FILLED':
            japanese = '約定済み'
        elif status == 'CANCELED_UNFILLED':
            japanese = '取消済'
        elif status == 'CANCELED_PARTIALLY_FILLED':
            japanese = '取消済(一部約定)'
        else:
            japanese = None
        return japanese
