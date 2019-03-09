from bitbank.functions import *
from bitbank.exceptions.schedcancel import SchedulerCancelException
from bitbank.order import Order
from bitbank.auto import Auto
from bitbank.apigateway import ApiGateway


class Prototype(Auto):

    DIVIDE_ORDER = 1
    PRICE_LIMIT = 3.0

    COMMISSION = 0.0015
    LOSS_CUT_PRICE = 0.5

    BUY_FAIL = 0.02
    SELL_FAIL = 0.02

    def __init__(self, adviser, pair, log):
        """
        :param adviser:       bitbank.adviser テクニカル分析結果から売却の指示をするクラスのインスタンス
        :param pair:          string          通貨のペア
        :param log:
        """
        super().__init__(adviser=adviser, pair=pair)
        self.order_ids = 0
        self.has_coin = False
        self.is_waiting = False
        self.waiting_price = None
        self.log = log
        self.api_gateway = ApiGateway()

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

    def request(self, operation, price, order_type):
        if operation == int(self.BUY):
            line_ = 'BUY         : {:<10}\n'.format(price)
            over_write_file(directory=self.log, line_=line_)
            self.buy(price=price, amount='hoge', order_type=order_type)

        elif operation == int(self.SELL):
            line_ = 'SELL        : {:<10}\n'.format(price)
            over_write_file(directory=self.log, line_=line_)
            self.sell(price=price, amount='hoge', order_type=order_type)

        elif operation == int(self.RETRY):
            # キャンセル
            result = self.cancel_orders(
                order_id=self.order_ids
            )
            # 再要求
            if result.side == 'buy':
                line_ = 'RETRY BUY  : {:<10}\n'.format(price)
                over_write_file(directory=self.log, line_=line_)
                self.buy(price=price, amount=result.remaining_amount, order_type=order_type)
            elif result.side == 'sell':
                line_ = 'RETRY SELL : {:<10}\n'.format(price)
                over_write_file(directory=self.log, line_=line_)
                self.sell(price=price, amount=result.remaining_amount, order_type=order_type)
        elif operation == int(self.STAY):
            pass
        else:
            raise SchedulerCancelException('operation fail')

    def check_request(self):
        if self.is_waiting:
            price = float(self.api_gateway.use_ticker(pair=self.pair)['last'])
            # 売り
            if self.has_coin:
                if self.waiting_price <= price:
                    self.waiting_price = None
                    self.is_waiting = False
                    self.contract_order_message()
            # 買い
            else:
                if self.waiting_price >= price:
                    self.waiting_price = None
                    self.is_waiting = False
                    self.contract_order_message()

    def buy(self, price, amount, order_type):
        self.new_orders(
            price=price,
            amount=amount,
            side='buy',
            order_type=order_type
        )
        self.buying_price = price
        self.has_coin = True

    def sell(self, price, amount, order_type):
        self.new_orders(
            price=price,
            amount=amount,
            side='sell',
            order_type=order_type
        )
        self.buying_price = None
        self.has_coin = False

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
            # Orderインスタンス化
            order = Order(
                order_id=0,
                pair=self.pair,
                side=side,
                type=order_type,
                price=price,
                start_amount=amount,
                remaining_amount=0,
                executed_amount=0,
                average_price=0,
                ordered_at=now(),
                status=''
            )

            self.new_order_message(order=order, retry=retry)
            self.order_ids += 1
            self.waiting_price = price
            self.is_waiting = True
            print()
            print(order.ordered_at + '   ' + side + ' ' + order.start_amount + ' ' + str(order.price))
        except Exception as e:
            print(e)
            self.error_message(message=e.args[0])
            raise SchedulerCancelException('Fail to order')

    def cancel_orders(self, order_id):
        """
        現在の注文をキャンセルする
        :param order_id:  number
        """
        try:
            # 強制的にsideを決める
            result = {
                'order_id': order_id,
                'side': self.__side(),
                'status': 'hoge',
                'pair': 'hoge',
                'price': 'hoge',
                'average_price': 'hoge',
                'start_amount': 'hoge',
                'executed_amount': 'hoge',
                'remaining_amount': 'hoge',
                'ordered_at': 'hoge',
                'type': 'hoge'
            }
            self.cancel_order_message(result=result)
            self.order_ids -= 1
            self.waiting_price = None
            self.is_waiting = False
            order = Order.order(r=result)
            return order
        except Exception as e:
            print(e)
            raise SchedulerCancelException('Fail to cancel order')

    def __side(self):
        if self.has_coin:
            return 'sell'
        elif self.has_coin:
            return 'buy'
