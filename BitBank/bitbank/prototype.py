from bitbank.functions import *
from bitbank.exceptions.schedcancel import SchedulerCancelException
from bitbank.order import Order
from bitbank.auto import Auto


class Prototype(Auto):

    DIVIDE_ORDER = 1
    PRICE_LIMIT = 3.0

    COMMISSION = 0.0015
    LOSS_CUT = 0.5

    BUY_FAIL = 0.02
    SELL_FAIL = 0.02

    def __init__(self, adviser, pair):
        """
        :param adviser:       bitbank.adviser テクニカル分析結果から売却の指示をするクラスのインスタンス
        :param pair:          string          通貨のペア
        """
        super().__init__(adviser=adviser, pair=pair)
        self.order_ids = 0
        self.has_coin = False

    def __call__(self):
        # 損切り
        self.loss_cut(coin='hoge')

        # データを更新
        self.adviser.fetch_recent_data()

        # 日本円があるとき、新規注文する
        if self.has_coin is False:
            operation, price = self.adviser.operation(
                has_coin=False
            )
            # STAYではないとき
            if operation == int(self.BUY):
                # 新規注文
                side = self.__operation_to_side(operation=operation)
                candidate = self.find_maker(side='bids')
                for i in range(self.DIVIDE_ORDER):
                    self.new_orders(
                        price=candidate[i],
                        amount='hoge',
                        side=side,
                        order_type=self.TYPE_LIMIT
                    )
                self.buying_price = price
                self.has_coin = True
            else:
                pass

        # コインがあるとき、新規注文する
        if self.has_coin:
            operation, price = self.adviser.operation(
                has_coin=True
            )
            # STAYではないとき
            if operation == int(self.SELL):
                # 新規注文
                side = self.__operation_to_side(operation=operation)
                candidate = self.find_maker(side='asks')
                for i in range(self.DIVIDE_ORDER):
                    self.new_orders(
                        price=candidate[i],
                        amount='hoge',
                        side=side,
                        order_type=self.TYPE_LIMIT
                    )
                self.buying_price = None
                self.has_coin = False
            else:
                pass

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
            result = {
                'side': 'hoge',
                'status': 'hoge',
                'pair': 'hoge',
                'price': 'hoge',
                'average_price': 'hoge',
                'start_amount': 'hoge',
                'executed_amount': 'hoge',
                'remaining_amount': 'hoge'
            }
            self.cancel_order_message(result=result)
            self.order_ids = None

            # 売り注文だったら成り行きで売り払う
            if result['side'] == 'sell':
                self.market_selling_message()
                self.new_orders(
                    price=result['price'],
                    amount=result['remaining_amount'],
                    side='sell',
                    order_type=self.TYPE_MARKET,
                )
        except Exception as e:
            print(e)
            raise SchedulerCancelException('Fail to cancel order')

    def loss_cut(self, coin):
        price = self.fetch_price()
        if self.buying_price is None:
            pass
        else:
            if price <= self.buying_price - self.LOSS_CUT:
                self.loss_cut_message()
                self.new_orders(
                    price=price,
                    amount=coin,
                    side='sell',
                    order_type=self.TYPE_MARKET
                )
                raise SchedulerCancelException("loss cut")

    def find_maker(self, side):
        """
        Maker手数料の候補を返す
        :return: list 取引値に近い順
        """
        result = self.api_gateway.use_depth(pair=self.pair)
        result = np.asarray(result[side], dtype=float)
        result = result[0:, 0]
        if side == 'asks':
            # 売り側
            # 小さい
            head = result[0]
            # 大きい
            tail = result[-1]
        elif side == 'bids':
            # 買い側
            # 大きい
            tail = result[0]
            # 小さい
            head = result[-1]
        else:
            raise TypeError('in find_maker')
        mask = np.arange(start=head, stop=tail, step=0.001, dtype=np.float64)
        mask = np.round(mask, decimals=3)
        result = np.round(result, decimals=3)
        inter_diff = np.setdiff1d(mask, result)
        if side == 'bids':
            inter_diff = inter_diff[::-1]
        return inter_diff
