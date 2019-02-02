import time
from bitbank.functions import *
from bitbank.exceptions.schedcancel import SchedulerCancelException
from bitbank.order import Order
from bitbank.auto import Auto


class Bot(Auto):
    DIVIDE_ORDER = 1
    PRICE_LIMIT = 3.0

    MANAGE_AMOUNT = 180000
    COMMISSION = 0.0015
    LOSS_CUT = 0.5

    BUY_FAIL = 0.02
    SELL_FAIL = 0.02

    def __init__(self, adviser, pair, api_key, api_secret):
        """
        :param adviser:       bitbank.adviser テクニカル分析結果から売却の指示をするクラスのインスタンス
        :param pair:          string          通貨のペア
        :param api_key:       string          APIキー
        :param api_secret     string          APIシークレットキー
        """
        super().__init__(adviser=adviser, pair=pair, api_key=api_key, api_secret=api_secret)

    def __call__(self):
        # 注文の情報を確認
        orders = self.fetch_orders()

        # 注文があった場合
        if orders is not False:
            # 約定していない注文をキャンセル(その後リストから削除)。成立していればリストから削除
            for order_id in orders:
                # 約定注文
                if orders[order_id].status == 'FULLY_FILLED':
                    # リストから削除
                    self.order_ids = None
                # 注文中
                else:
                    # オーダーをキャンセルしない
                    price = self.fetch_price()
                    # 買い損ねたとき
                    if float(orders[order_id].price) + self.BUY_FAIL <= price and orders[order_id].side == 'buy':
                        self.cancel_orders(order_id=order_id)
                    elif float(orders[order_id].price) - self.SELL_FAIL >= price and orders[order_id].side == 'sell':
                        self.cancel_orders(order_id=order_id)

        # アセットを読み込む
        assets_free_amount = self.fetch_asset()

        # 損切り
        self.loss_cut(float(assets_free_amount[self.coin]))

        # データを更新
        self.adviser.fetch_recent_data()

        # 日本円があるとき、新規注文する
        if float(assets_free_amount[self.yen]) > self.MANAGE_AMOUNT:
            operation, price = self.adviser.operation(
                has_coin=False
            )
            # STAYではないとき
            if operation == int(self.BUY):
                # 新規注文
                if self.can_order():
                    side = self.__operation_to_side(operation=operation)
                    candidate = self.find_maker(side='bids')
                    for i in range(self.DIVIDE_ORDER):
                        amount = float(self.MANAGE_AMOUNT / price / self.DIVIDE_ORDER)
                        self.new_orders(
                            price=candidate[i],
                            amount=amount,
                            side=side,
                            order_type=self.TYPE_LIMIT
                        )
                    self.buying_price = price
                else:
                    raise SchedulerCancelException('price belows the limit. ')
            else:
                pass

        # コインがあるとき、新規注文する
        if float(assets_free_amount[self.coin]) > 0:
            operation, price = self.adviser.operation(
                has_coin=True
            )
            # STAYではないとき
            if operation == int(self.SELL):
                # 新規注文
                if self.can_order():
                    side = self.__operation_to_side(operation=operation)
                    candidate = self.find_maker(side='asks')
                    for i in range(self.DIVIDE_ORDER):
                        self.new_orders(
                            price=candidate[i],
                            amount=(float(assets_free_amount[self.coin]) / self.DIVIDE_ORDER),
                            side=side,
                            order_type=self.TYPE_LIMIT
                        )
                    self.buying_price = None
                else:
                    raise SchedulerCancelException('price belows the limit. ')

            else:
                pass

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

            self.new_order_message(order=order, retry=retry)
            self.order_ids = result['order_id']
            print()
            print(order.ordered_at + '   ' + side + ' ' + order.start_amount + ' ' + order.price)
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
            if '50010'in e.args[0]:
                self.__line(message='キャンセルできませんでした。')
            else:
                raise SchedulerCancelException('Fail to cancel order')

    def fetch_orders(self):
        """
        現在の注文の状況を確認する
        :return: False | list  注文が存在すればその情報、なければFalse
        {
            'order_id_1': bitbank.order.Order,
            'order_id_2': bitbank.order.Order,
        }
        """
        if self.order_ids is None:
            return False
        results = self.api_gateway.use_orders_info(
            pair=self.pair,
            order_ids=[self.order_ids]
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

    def can_order(self):
        """
        開始時よりも価格が大幅に下がった時に強制終了させるためのメソッド
        :return: bool:
        """
        price = self.fetch_price()
        if price >= (self.__start_price - self.PRICE_LIMIT):
            return True
        else:
            # 全てのコインを売る
            assets_free_amount = self.fetch_asset()
            self.new_orders(
                price=price,
                amount=assets_free_amount[self.coin],
                side='sell',
                order_type=self.TYPE_MARKET
            )
            message = "開始時の価格を大きく下回りました。\n" \
                      "取引を中止します。 \n" \
                      "===================\n" \
                      "時刻: {}\n" \
                      "===================".format(
                       now()
                       )
            message.replace('n', '%0D%0A')
            self.__line(message=message)
            return False
