from bitbank.adviser.adviser import Adviser
from bitbank.adviser.functions import *
from bitbank.functions import read_file
from bitbank.exceptions.tagexception import DataNotUpdateException


class Tag(Adviser):
    ASKS = 'asks'
    BIDS = 'bids'

    def __init__(self, ema_term, ma_term, buy_directory, sell_directory, price_range=0.1):
        """
        :param ema_term:
        :param ma_term:
        :param buy_directory:
        :param sell_directory:
        :param price_range:
        """
        super().__init__()
        # 設定
        self.ema_term = ema_term
        self.ma_term = ma_term
        self.buy_genome = read_file(directory=buy_directory).get_elite_genome()
        self.sell_genome = read_file(directory=sell_directory).get_elite_genome()
        self.price_range = price_range
        # データ
        # 直近
        self.ma = None
        self.ema = None
        self.price = None
        # 直近より以前
        self.ma_list = None
        self.ema_list = None
        self.data = None
        # 作業
        self.fetch_count = 0
        self.__is_update_data = False

        self.tag_candlestick()

    def should_cancel(self, price, has_coin, buying_price):
        guess_ma = self.guess_ma(price=price)
        guess_ema = self.guess_ema(price=price)
        inc, e = self.guess_ma_regression(guess_ma=guess_ma)
        ema_price_diff = self.guess_ema_price_diff(ema=guess_ema, price=price)
        ema_ma_diff = self.guess_ema_ma_diff(ema=guess_ema, ma=guess_ma)
        ma_diff = self.guess_ma_diff(guess_ma=guess_ma)
        ema_diff = self.guess_ema_diff(guess_ema=guess_ema)
        ema_inc, ema_e = self.guess_ema_regression(guess_ema=guess_ema)
        # is_waiting = False なので、BUY, SELL, STAY のうちどれか
        operation, order_price, order_type = self.analysis(
            inc=inc,
            e=e,
            ema_price_diff=ema_price_diff,
            ema_ma_diff=ema_ma_diff,
            ma_diff=ma_diff,
            ema_inc=ema_inc,
            ema_e=ema_e,
            ema_diff=ema_diff,
            price=price,
            has_coin=has_coin,
            is_waiting=False,
            buying_price=buying_price,
            waiting_price=price
        )
        if operation == self.BUY or operation == self.SELL:
            return False
        elif operation == self.STAY:
            return True

    def operation(self, has_coin, is_waiting, buying_price, waiting_price, price=None):
        if price is None:
            price = self.api_gateway.use_ticker(pair=self.pair)
            price = float(price['last'])
        # 毎回更新
        self.price = price
        self.is_update_data(True)
        self.update_ma()
        self.update_ema()
        # 分析
        inc, e = self.ma_regression()
        ema_price_diff = self.ema_price_diff()
        ema_ma_diff = self.ema_ma_diff()
        ma_diff = self.ma_diff()
        ema_inc, ema_e = self.ema_regression()
        price_inc, price_e = self.price_regression()
        print('price         : {:.5f}'.format(self.price))
        print('ema           : {:.5f}'.format(self.ema))
        print('ma            : {:.5f}'.format(self.ma))

        print('inc           : {:.5f}'.format(inc))
        print('e             : {:.5f}'.format(e))
        print('ema price diff: {:.5f}'.format(ema_price_diff))
        print('ema ma diff   : {:.5f}'.format(ema_ma_diff))
        print('ma diff       : {:.5f}'.format(ma_diff))
        print('ema inc       : {:.5f}'.format(ema_inc))
        print('ema e         : {:.5f}'.format(ema_e))
        print('price inc     : {:.5f}'.format(price_inc))
        print('price e       : {:.5f}'.format(price_e))

        # 間隔更新
        self.fetch_count += 0
        if self.fetch_count >= 60:
            self.fetch_count = 0
            self.update_data()
            self.update_ma_list()
            self.update_ema_list()

        self.is_update_data(False)

        # 複数分析
        if has_coin:
            board = self.find_maker(side=self.ASKS)
            board = [i for i in board if i <= (board[0] + self.price_range)]
        else:
            board = self.find_maker(side=self.BIDS)
            board = [i for i in board if i >= (board[0] - self.price_range)]

        sell_retrys = list()

        for price in board:
            guess_ma = self.guess_ma(price=price)
            guess_ema = self.guess_ema(price=price)
            inc, e = self.guess_ma_regression(guess_ma=guess_ma)
            ema_price_diff = self.guess_ema_price_diff(ema=guess_ema, price=price)
            ema_ma_diff = self.guess_ema_ma_diff(ema=guess_ema, ma=guess_ma)
            ma_diff = self.guess_ma_diff(guess_ma=guess_ma)
            ema_diff = self.guess_ema_diff(guess_ema=guess_ema)
            ema_inc, ema_e = self.guess_ema_regression(guess_ema=guess_ema)
            price_inc, price_e = self.guess_price_regression(guess_price=price)
            operation, order_price, order_type = self.analysis(
                inc=inc,
                e=e,
                ema_price_diff=ema_price_diff,
                ema_ma_diff=ema_ma_diff,
                ma_diff=ma_diff,
                ema_inc=ema_inc,
                ema_e=ema_e,
                ema_diff=ema_diff,
                price=price,
                price_inc=price_inc,
                price_e=price_e,
                has_coin=has_coin,
                is_waiting=is_waiting,
                buying_price=buying_price,
                waiting_price=waiting_price
            )
            if operation == self.BUY or operation == self.SELL:
                print('PRICE: {:.5f} 1'.format(order_price))
                return operation, order_price, order_type
            elif operation == self.RETRY and not has_coin:

                print('PRICE: {:.5f} 1'.format(order_price))
                return operation, order_price, order_type
            # 売りのリトライ
            elif has_coin and operation == self.RETRY:
                sell_retrys.append({'operation': operation, 'price': float(order_price), 'order_type': order_type})
            else:
                pass

        if len(sell_retrys) > 0:
            true_ = [i for i in sell_retrys if i['price'] > buying_price]
            # buying_priceを超えるものがある
            if len(true_) > 0:
                return true_[0]['operation'], true_[0]['price'], true_[0]['order_type']
            # 超えるものがない
            else:
                return sell_retrys[0]['operation'], sell_retrys[0]['price'], sell_retrys[0]['order_type']

        return self.STAY, None, None

    def analysis(self, inc, e, ema_price_diff, ema_ma_diff, ma_diff, price, has_coin, is_waiting, buying_price, waiting_price, ema_diff, ema_inc, ema_e, price_inc, price_e):
        """
        分析して指示を出す
        :param inc: float 傾き
        :param e: float 誤差
        :param ema_price_diff: float PRICEとEMA
        :param ema_ma_diff: float MAとEMA
        :param ma_diff: 直前のMAの傾き
        :param price: 価格
        :param has_coin: bool
        :param is_waiting: bool
        :param buying_price: float|None
        :param waiting_price:
        :return: const int, float, const string
        """
        # 売り
        if has_coin:
            operation = self.sell_genome.operation(
                inc=inc,
                e=e,
                ema_price_diff=ema_price_diff,
                ema_ma_diff=ema_ma_diff,
                ma_diff=ma_diff,
                ema_inc=ema_inc,
                ema_e=ema_e,
                ema_diff=ema_diff,
                price=self.price - buying_price,
                price_inc=price_inc,
                price_e=price_e
            )
            if operation:
                if is_waiting:
                    if waiting_price > price:
                        return self.RETRY, price, self.TYPE_LIMIT
                else:
                    return self.SELL, price, self.TYPE_LIMIT
        # 買い
        else:
            operation = self.buy_genome.operation(
                inc=inc,
                e=e,
                ema_price_diff=ema_price_diff,
                ema_ma_diff=ema_ma_diff,
                ma_diff=ma_diff,
                ema_inc=ema_inc,
                ema_e=ema_e,
                ema_diff=ema_diff,
                price_inc=price_inc,
                price_e=price_e
            )
            if operation:
                # リトライ
                if is_waiting:
                    if waiting_price < price:
                        return self.RETRY, price, self.TYPE_LIMIT
                # 新規
                else:
                    return self.BUY, price, self.TYPE_LIMIT

        return self.STAY, None, None

    def guess_ma(self, price):
        return simple_moving_average(data=np.append(self.data, price), term=self.ma_term)[0]

    def guess_ema(self, price):
        return self.ema_list[-1] + (2 / (self.ema_term + 1)) * (price - self.ema_list[-1])

    def guess_ma_diff(self, guess_ma):
        return guess_ma - self.ma_list[-1]

    def guess_ema_diff(self, guess_ema):
        return guess_ema - self.ema_list[-1]

    def guess_price_regression(self, guess_price):
        price_list = np.append(self.data, guess_price)
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(price_list))
        w = linear_regression(x=x, t=price_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - price_list
        e = e * e.T
        e = np.sum(e)
        return w[1], e

    def guess_ema_regression(self, guess_ema):
        ema_list = np.append(self.ema_list, guess_ema)
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(ema_list))
        w = linear_regression(x=x, t=ema_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - ema_list
        e = e * e.T
        e = np.sum(e)
        return w[1], e

    def guess_ma_regression(self, guess_ma):
        ma_list = np.append(self.ma_list, guess_ma)
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(ma_list))
        w = linear_regression(x=x, t=ma_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - ma_list
        e = e * e.T
        e = np.sum(e)
        return w[1], e

    @staticmethod
    def guess_ema_price_diff(ema, price):
        return ema - price

    @staticmethod
    def guess_ema_ma_diff(ema, ma):
        return ema - ma

    def find_maker(self, side):
        """
        Maker手数料の候補を返す
        :return: list 取引値に近い順
        """
        result = self.api_gateway.use_depth(pair=self.pair)
        result = np.asarray(result[side], dtype=float)
        result = result[0:, 0]
        if side == self.ASKS:
            # 売り側
            # 小さい
            head = result[0]
            # 大きい
            tail = result[-1]
        elif side == self.BIDS:
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
        if side == self.BIDS:
            inter_diff = inter_diff[::-1]
        return inter_diff

    def tag_candlestick(self):
        """
        EMA,MAのDataFrame
        :return:
        """
        ma = simple_moving_average(data=self.candlestick.end.values.astype(float), term=self.ma_term)
        self.ma_list = ma[-1 * self.ma_term + 1:-1]
        self.ma = ma[-1]
        ema = exponential_moving_average(data=self.candlestick.end.values.astype(float), term=self.ema_term)
        self.ema_list = ema[-1 * self.ema_term:-1]
        self.ema = ema[-1]
        self.data = self.candlestick.end.values.astype(float)[-1 * self.ma_term + 1:]

    def ma_diff(self):
        """
        MAの直前の傾き
        :return:
        """
        return self.ma - self.ma_list[-1]

    def price_regression(self):
        """
        ~n-1の線形回帰直線と二乗和誤差
        :return: 傾き, 誤差
        """
        price_list = np.append(self.data, self.price)
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(price_list))
        w = linear_regression(x=x, t=price_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - price_list
        e = e * e.T
        e = np.sum(e)
        return w[1], e

    def ema_regression(self):
        """
        ~n-1の線形回帰直線と二乗和誤差
        :return: 傾き, 誤差
        """
        ema_list = np.append(self.ema_list, self.ema)
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(ema_list))
        w = linear_regression(x=x, t=ema_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - ema_list
        e = e * e.T
        e = np.sum(e)
        return w[1], e

    def ma_regression(self):
        """
        ~n-1の線形回帰直線と二乗和誤差
        :return: 傾き, 誤差
        """
        ma_list = np.append(self.ma_list, self.ma)
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(ma_list))
        w = linear_regression(x=x, t=ma_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - ma_list
        e = e * e.T
        e = np.sum(e)
        return w[1], e

    def ema_price_diff(self):
        """
        EMAとPRICEの乖離率
        :return: float
        """
        if self.can_access_data():
            return self.ema - self.price
        else:
            raise DataNotUpdateException()

    def ema_ma_diff(self):
        """
        EMAとMAの乖離率
        :return: float
        """
        return self.ema - self.ma

    def update_data(self):
        """
        データを更新。一番古いデータを捨て、新しいデータを末尾に追加
        :return:
        """
        if self.can_access_data():
            self.data = np.delete(self.data, 0)
            self.data = np.append(self.data, self.price)
        else:
            raise DataNotUpdateException()

    def update_ma_list(self):
        self.ma_list = np.delete(self.ma_list, 0)
        self.ma_list = np.append(self.ma_list, self.ma)

    def update_ema_list(self):
        self.ema_list = np.delete(self.ema_list, 0)
        self.ema_list = np.append(self.ema_list, self.ema)

    def update_ma(self):
        if self.can_access_data():
            self.ma = simple_moving_average(data=np.append(self.data, self.price), term=self.ma_term)[0]
        else:
            raise DataNotUpdateException()

    def update_ema(self):
        if self.can_access_data():
            self.ema = self.ema_list[-1] + (2 / (self.ema_term + 1)) * (self.price - self.ema_list[-1])
        else:
            raise DataNotUpdateException()

    def is_update_data(self, is_update):
        """
        データ更新をしたかを決める
        :param is_update: bool
        :return:
        """
        self.__is_update_data = is_update

    def can_access_data(self):
        """
        データを更新したのちはアクセス可能
        :return:
        """
        return self.__is_update_data

