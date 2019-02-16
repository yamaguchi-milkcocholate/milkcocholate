from bitbank.functions import *
from bitbank.exceptions.schedcancel import SchedulerCancelException
from bitbank.order import Order
from bitbank.auto import Auto


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
        self.log = log

    def __call__(self):
        # 指示を受ける
        operation, price, order_type = self.adviser.operation(
            has_coin=self.has_coin,
            is_waiting=self.is_waiting,
            buying_price=self.buying_price
        )

        if operation == int(self.BUY):
            line_ = 'BUY         : {:<10}'.format(price)
            over_write_file(directory='../15min/log/' + self.log, line_=line_)
            self.buy(price=price, amount='hoge', order_type=order_type)

        elif operation == int(self.SELL):
            line_ = 'SELL        : {:<10}'.format(price)
            over_write_file(directory='../15min/log/' + self.log, line_=line_)
            self.sell(price=price, amount='hoge', order_type=order_type)

        elif operation == int(self.RETRY):
            # キャンセル
            result = self.cancel_orders(
                order_id=self.order_ids
            )
            # 再要求
            if result.side == 'buy':
                line_ = 'RETRY BUY  : {:<10}'.format(price)
                over_write_file(directory='../15min/log/' + self.log, line_=line_)
                self.buy(price=price, amount=result.remaining_amount, order_type=order_type)
            elif result.side == 'sell':
                line_ = 'RETRY SELL : {:<10}'.format(price)
                over_write_file(directory='../15min/log/' + self.log, line_=line_)
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
            print()
            print(order.ordered_at + '   ' + side + ' ' + order.start_amount + ' ' + order.price)
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
                'ordered_at': 'hoge'
            }
            self.cancel_order_message(result=result)
            self.order_ids = None
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
