import time
from bitbank.functions import *
from bitbank.exceptions.schedcancel import SchedulerCancelException
from bitbank.order import Order
from bitbank.auto import Auto


class Bot(Auto):
    MANAGE_AMOUNT = 190000
    LOSS_CUT_PRICE = 0.5

    def __init__(self, adviser, pair, api_key, api_secret, log):
        """
        :param adviser:       bitbank.adviser テクニカル分析結果から売却の指示をするクラスのインスタンス
        :param pair:          string          通貨のペア
        :param api_key:       string          APIキー
        :param api_secret     string          APIシークレットキー
        :param log
        """
        super().__init__(adviser=adviser, pair=pair, api_key=api_key, api_secret=api_secret)
        self.order_id = 0
        self.has_coin = False
        self.is_waiting = False
        self.waiting_price = None
        self.log = log

    def __call__(self):
        # 要求を確認
        self.check_request()
        # 指示を受ける
        operation, price, order_type = self.adviser.operation(
            has_coin=self.has_coin,
            is_waiting=self.is_waiting,
            buying_price=self.buying_price,
            waiting_price=self.waiting_price
        )
        self.request(operation=operation, price=price, order_type=order_type)

    def check_request(self):
        # 注文があった場合
        if self.is_waiting:
            # 注文の情報を確認
            order = self.fetch_order()
            side = order.side
            if side == 'buy':
                if order.status == 'FULLY_FILLED':
                    # 削除
                    self.order_id = None
                    self.waiting_price = None
                    self.is_waiting = False
                    self.has_coin = True
                    self.buying_price = float(order.price)
                # 注文中
                else:
                    pass
            elif side == 'sell':
                if order.status == 'FULLY_FILLED':
                    # 削除
                    self.order_id = None
                    self.waiting_price = None
                    self.is_waiting = False
                    self.has_coin = False
                    self.buying_price = None
                # 注文中
                else:
                    pass

    def request(self, operation, price, order_type):
        assets_free_amount = self.fetch_asset()
        # 損切
        self.loss_cut(assets_free_amount[self.coin])
        if operation == int(self.BUY):
            line_ = 'BUY         : {:<10}'.format(price) + now() + '  ' + str(order_type) + '\n'
            over_write_file(directory=self.log, line_=line_)
            amount = float(self.MANAGE_AMOUNT / price)
            self.buy(price=price, amount=amount, order_type=order_type)

        elif operation == int(self.SELL):
            line_ = 'SELL        : {:<10}'.format(price) + now() + '  ' + str(order_type) + '\n'
            over_write_file(directory=self.log, line_=line_)
            amount = float(assets_free_amount[self.coin])
            self.sell(price=price, amount=amount, order_type=order_type)

        elif operation == int(self.RETRY):
            # キャンセル
            result = self.cancel_orders(
                order_id=self.order_id
            )
            # 再要求
            if result.side == 'buy':
                line_ = 'RETRY BUY   : {:<10}'.format(price) + now() + '  ' + str(order_type) + '\n'
                over_write_file(directory=self.log, line_=line_)
                self.buy(price=price, amount=result.remaining_amount, order_type=order_type)
            elif result.side == 'sell':
                line_ = 'RETRY SELL  : {:<10}'.format(price) + now() + '  ' + str(order_type) + '\n'
                over_write_file(directory=self.log, line_=line_)
                self.sell(price=price, amount=result.remaining_amount, order_type=order_type)
        elif operation == int(self.STAY):
            pass
        else:
            raise SchedulerCancelException('operation fail')

    def buy(self, price, amount, order_type):
        self.new_orders(
            price=price,
            amount=amount,
            side='buy',
            order_type=order_type
        )

    def sell(self, price, amount, order_type):
        self.new_orders(
            price=price,
            amount=amount,
            side='sell',
            order_type=order_type
        )

    def loss_cut(self, coin):
        price = self.fetch_price()
        if self.buying_price is None:
            pass
        else:
            if price <= self.buying_price - self.LOSS_CUT_PRICE:
                self.loss_cut_message()
                self.new_orders(
                    price=price,
                    amount=coin,
                    side='sell',
                    order_type=self.TYPE_MARKET
                )
                raise SchedulerCancelException("loss cut")

    def fetch_asset(self):
        """
        アセットの利用可能な量を読み込む
        DBにアセットを書き込む(YEN, XRP)
        insert_list[''] = [
            'coin', 'amount', 'price', 'time'
        ]
        :return: dict 利用可能な量
        """
        results = self.api_gateway.use_asset()
        assets = dict()
        insert_list = {self.coin: [self.coin], self.yen: [self.yen]}
        for result in results['assets']:
            if result['asset'] == self.coin:
                assets[self.coin] = result['free_amount']
                insert_list[self.coin].append(result['onhand_amount'])
            elif result['asset'] == self.yen:
                assets[self.yen] = result['free_amount']
                insert_list[self.yen].append(result['onhand_amount'])
        ticker = self.fetch_price()
        insert_list[self.coin].append(ticker)
        insert_list[self.yen].append(ticker)
        insert_list[self.coin].append(now())
        insert_list[self.yen].append(now())
        return assets

    def new_orders(self, price, amount, side, order_type, retry=0):
        """
        新規注文を行う
        :param price:      number
        :param amount:     number
        :param side:       string
        :param order_type: string
        :param retry:      integer
        """
        try:
            result = self.api_gateway.new_order(
                pair=self.pair,
                price=price,
                amount=amount,
                side=side,
                order_type=order_type
            )
            # Orderインスタンス化
            order = Order.order(r=result)

            self.new_order_message(order=order, retry=retry)
            self.order_id = result['order_id']
            self.waiting_price = price
            self.is_waiting = True
            print()
            print(str(order.ordered_at) + '   ' + str(side) + ' ' + str(order.start_amount) + ' ' + str(order.price))
        except Exception as e:
            print(e)
            if '60002' in e.args[0]:
                #  60002 内容: 成行買い注文の数量上限を上回っています
                amount = float(amount) / 2.0
                # 数量が10.0以上の場合のみ
                if amount > 10.0:
                    self.new_orders(price, amount, side, order_type, retry=retry + 1)
                    # 連続して成り行き注文すると怒られる
                    time.sleep(5)
                    self.new_orders(price, amount, side, order_type, retry=retry + 1)
                else:
                    pass
            elif '70009' in e.args[0] or '70011' in e.args[0]:
                # 70009 ただいま成行注文を一時的に制限しています。指値注文をご利用ください
                # 70011 ただいまリクエストが混雑してます。しばらく時間を空けてから再度リクエストをお願いします
                print()
                print('5秒の遅らせて再度注文します。')
                self.__line(message='5秒の遅らせて再度注文します。')
                time.sleep(5)
                self.new_orders(price, amount, side, order_type, retry=retry + 1)
            elif '60004' in e.args[0]:
                #  60004 内容: 指定した数量がしきい値を下回っています
                pass
            else:
                self.error_message(message=e.args[0])
                raise SchedulerCancelException('Fail to order')

    def cancel_orders(self, order_id):
        """
        現在の注文をキャンセルする
        :param order_id:  number
        """
        try:
            result = self.api_gateway.cancel_order(
                pair=self.pair,
                order_id=order_id
            )
            self.cancel_order_message(result=result)
            self.order_id = None
            self.waiting_price = None
            self.is_waiting = False
            # Orderインスタンス化
            order = Order.order(r=result)
            return order

        except Exception as e:
            print(e)
            if '50010'in e.args[0]:
                self.__line(message='キャンセルできませんでした。')
            else:
                raise SchedulerCancelException('Fail to cancel order')

    def fetch_order(self):
        """
        現在の注文の状況を確認する
        :return: False | Order  注文が存在すればその情報、なければFalse
        """
        if self.order_id is None:
            return False
        result = self.api_gateway.use_order(
            pair=self.pair,
            order_id=self.order_id
        )
        if result is None:
            raise SchedulerCancelException('Fail to get orders information')

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
