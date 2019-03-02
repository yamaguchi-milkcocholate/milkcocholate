from bitbank.adviser.adviser import Adviser
from bitbank.adviser.functions import *
from bitbank.functions import read_file
from bitbank.exceptions.tagexception import DataNotUpdateException


class Tag(Adviser):
    ASKS = 'asks'
    BIDS = 'bids'
    PROFIT = 0.15

    def __init__(self, ema_term, ma_term, buy_directory, sell_directory):
        """
        :param ema_term:
        :param ma_term:
        :param buy_directory:
        :param sell_directory:
        """
        super().__init__()
        # 設定
        self.ema_term = ema_term
        self.ma_term = ma_term
        self.buy_genome = read_file(directory=buy_directory).get_elite_genome()
        self.sell_genome = read_file(directory=sell_directory).get_elite_genome()
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
        self.__price_more_than_ema = None
        self.__ema_price_trend_count = 0

        self.tag_candlestick()

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
        print('inc           : {:.5f}'.format(inc))
        print('e             : {:.5f}'.format(e))
        print('ema price diff: {:.5f}'.format(ema_price_diff))
        print('ema ma diff   : {:.5f}'.format(ema_ma_diff))
        print('ma diff       : {:.5f}'.format(ma_diff))
        if has_coin:
            board = self.find_maker(side=self.ASKS)
        else:
            board = self.find_maker(side=self.BIDS)

        operation, price, order_type = self.analysis(
            inc=inc,
            e=e,
            ema_price_diff=ema_price_diff,
            ema_ma_diff=ema_ma_diff,
            ma_diff=ma_diff,
            board=board,
            has_coin=has_coin,
            is_waiting=is_waiting,
            buying_price=buying_price,
            waiting_price=waiting_price
        )

        # 間隔更新
        self.fetch_count += 0
        if self.fetch_count >= 15:
            self.fetch_count = 0
            self.update_data()
            self.update_ma_list()
            self.update_ma_list()

        self.is_update_data(False)
        return operation, price, order_type

    def analysis(self, inc, e, ema_price_diff, ema_ma_diff, ma_diff, board, has_coin, is_waiting, buying_price, waiting_price):
        """
        分析して指示を出す
        :param inc: float 傾き
        :param e: float 誤差
        :param ema_price_diff: float PRICEとEMA
        :param ema_ma_diff: float MAとEMA
        :param ma_diff: 直前のMAの傾き
        :param board: list 板情報
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
                price=self.price - buying_price
            )
            if operation:
                if is_waiting:
                    if waiting_price < board[0]:
                        return self.RETRY, board[0], self.TYPE_LIMIT
                else:
                    return self.SELL, board[0], self.TYPE_LIMIT
        # 買い
        else:
            operation = self.buy_genome.operation(
                inc=inc,
                e=e,
                ema_price_diff=ema_price_diff,
                ema_ma_diff=ema_ma_diff,
                ma_diff=ma_diff
            )
            if operation:
                # リトライ
                if is_waiting:
                    if waiting_price > board[0]:
                        return self.RETRY, board[0], self.TYPE_LIMIT
                # 新規
                else:
                    return self.BUY, board[0], self.TYPE_LIMIT

        return self.STAY, None, None

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
        self.ma_list = ma[-1 * self.ma_term:-1]
        self.ma = ma[-1]
        ema = exponential_moving_average(data=self.candlestick.end.values.astype(float), term=self.ema_term)
        self.ema_list = ema[-1 * self.ema_term:-1]
        self.ema = ema[-1]
        self.data = self.candlestick.end.values.astype(float)[-1 * self.ma_term + 1:]

    def guess_price_ma(self, ma):
        """
        MAを入力して、PRICEを出力
        :param ma: MA
        :return: PRICE
        """
        return self.ma_term * ma - np.sum(self.data)

    def guess_price_ema(self, ema):
        """
        EMAを入力して、PRICEを出力
        :return:
        """
        ema_n_1 = self.ema_list[-1]
        return ema_n_1 + ((self.ema_term - 1) / 2)(ema - ema_n_1)

    def ma_diff(self):
        """
        MAの直前の傾き
        :return:
        """
        return self.ma - self.ma_list[-1]

    def ma_regression(self):
        """
        ~n-1の線形回帰直線と二乗和誤差
        :return: 傾き, 誤差
        """
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(self.ma_list))
        w = linear_regression(x=x, t=self.ma_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - self.ma_list
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

