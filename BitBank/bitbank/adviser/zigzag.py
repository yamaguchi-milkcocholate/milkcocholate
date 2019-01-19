from bitbank.apigateway import ApiGateway
import pandas as pd
from pytz import timezone
import datetime


class ZigZagAdviser:
    BUY = 1
    STAY = 2
    SELL = 3

    TOP = 10   # 値幅率を超えて上がっているときの状態
    BOTTOM = 11   # 値幅率を超えて下がっているときの状態
    OTHER = 12

    TOP_DECISION_TERM = 60   # 15min
    BOTTOM_DECISION_TERM = 200   # 50min

    FETCH_TERM = 4  # 4 /min
    CANDLESTICK = 15  # 15min

    def __init__(self, pair='xrp_jpy', candle_type='15min', buying_price=None, limit=None):
        self.__pair = pair
        self.__candle_type = candle_type
        self.__api_gateway = ApiGateway()
        self.genome = None
        self.depth = None
        self.buy_deviation = None
        self.sell_deviation = None
        self.rsi_term = None
        self.rsi_data = None
        self.rsi_step = None
        self.rsi_bottom = None
        self.max_high = None
        self.min_low = None
        self.max_high_i = None
        self.min_low_i = None
        self.top_i = None
        self.bottom_i = None
        self.last_depth = None
        self.data_i = None
        self.price = None
        self.trend = None
        self.buying_price = buying_price
        self.limit = limit
        self.decision_term = 0
        self.candlestick = self.make_price_data_frame()

    def __call__(self, *args, **kwargs):
        self.is_candlestick = True
        self.zigzag_candlestick()
        self.is_candlestick = False
        self.candlestick = None

    def operation(self, has_coin):
        # 売りのエントリー
        if self.trend == self.TOP and has_coin:
            operation = self.SELL
            return operation, self.price

        # 買いのエントリー
        elif self.trend == self.BOTTOM and not has_coin:
            operation = self.BUY
            self.buying_price = self.price
            return operation, self.price

        elif self.trend == self.OTHER:
            operation = self.STAY
            return operation, self.price
        else:
            operation = self.STAY
            return operation, self.price

    def fetch_recent_data(self, price=None):
        """
        現在のtickerのapiを叩いて、最新の取引値を追加してデータを更新する
        """
        self.data_i += 1
        if price is None:
            price = self.__api_gateway.use_ticker(pair=self.__pair)
            price = float(price['last'])

        self.__update_min_max(high=price, low=price, i=self.data_i)
        self.price = price
        # RSI
        self.__fetch_rsi()

        self.__trend()

    def __fetch_rsi(self):
        self.rsi_step += 1
        # 新たな区間を追加
        if self.rsi_step == self.FETCH_TERM * self.CANDLESTICK:
            self.rsi_step = 0
            del self.rsi_data[0]
            self.rsi_data.append({
                'start': self.price,
                'end': self.price,
            })
        # 最後の区間を更新
        else:
            self.rsi_data[-1]['end'] = self.price

    def zigzag_candlestick(self):
        self.max_high = float(self.candlestick.loc[0].high)
        self.min_low = float(self.candlestick.loc[0].low)
        self.max_high_i = 0
        self.min_low_i = 0
        self.top_i = 0
        self.bottom_i = 0
        self.last_depth = 10**3   # 適当な大きさ

        for data_i in range(1, len(self.candlestick)):
            self.data_i = data_i
            high = float(self.candlestick.loc[data_i].high)
            low = float(self.candlestick.loc[data_i].low)

            self.__update_min_max(high=high, low=low, i=data_i)

            self.__trend(high=high, low=low)

        # RSI
        self.rsi_data = list()
        for data_i in range(len(self.candlestick) - self.rsi_term, len(self.candlestick)):
            self.rsi_data.append({
                'start': float(self.candlestick[data_i].start),
                'end': float(self.candlestick[data_i].end)
            })
        self.rsi_step = 0

    def rsi(self):
        plus = list()
        minus = list()
        for data in self.rsi_data:
            diff = data['end'] - data['start']
            if diff >= 0:
                plus.append(diff)
            else:
                minus.append(-1 * diff)
        if len(plus) > 0:
            plus = sum(plus)
        else:
            plus = 0
        if len(minus) > 0:
            minus = sum(minus)
        else:
            minus = 0
        plus = plus / self.rsi_term
        minus = minus / self.rsi_term
        return plus / (plus + minus) * 100

    def __update_min_max(self, high, low, i):
        if self.max_high < high:
            self.max_high = high
            self.max_high_i = i
        if self.min_low > low:
            self.min_low = low
            self.min_low_i = i

    def __top(self):
        """
        値幅率を超えて上がったときにTrue
        :return:
        """
        if self.buying_price is None or self.is_candlestick:
            return self.__and_gate(
                self.min_low * (1 + self.sell_deviation) < self.max_high,
                self.min_low_i < self.max_high_i,
                self.last_depth + (self.max_high_i - self.bottom_i) > self.depth,
            )
        else:
            return self.__and_gate(
                self.min_low * (1 + self.sell_deviation) < self.max_high,
                self.min_low_i < self.max_high_i,
                self.last_depth + (self.max_high_i - self.bottom_i) > self.depth,
                self.buying_price <= self.price
            )

    def __bottom(self):
        """
        値幅率を超えて下がったときにTrue
        :return:
        """
        rsi = self.rsi()
        if self.limit is None or self.is_candlestick:
            return self.__and_gate(
                self.max_high * (1 - self.buy_deviation) > self.min_low,
                self.max_high_i < self.min_low_i,
                self.last_depth + (self.min_low_i - self.top_i) > self.depth,
                self.rsi_bottom >= rsi
            )
        else:
            return self.__and_gate(
                self.max_high * (1 - self.buy_deviation) > self.min_low,
                self.max_high_i < self.min_low_i,
                self.last_depth + (self.min_low_i - self.top_i) > self.depth,
                self.limit >= self.price,
                self.rsi_bottom >= rsi
            )

    def __trend(self, high=None, low=None):
        if high is None:
            high = self.price
        if low is None:
            low = self.price

        self.trend = self.OTHER

        if self.__top():
            # 最大値更新
            if high >= self.max_high:
                self.decision_term = 0
            else:
                self.decision_term += 1
                # 山を決定
                if self.decision_term >= self.TOP_DECISION_TERM:
                    self.decision_term = 0
                    self.trend = self.TOP
                    self.top_i = self.max_high_i
                    self.last_depth = self.max_high_i - self.bottom_i
                    self.min_low = low
                    self.min_low_i = self.data_i

        elif self.__bottom():
            # 最小値更新
            if low <= self.min_low:
                self.decision_term = 0
            else:
                self.decision_term += 1
                # 谷を決定
                if self.decision_term >= self.BOTTOM_DECISION_TERM:
                    self.decision_term = 0
                    self.trend = self.BOTTOM
                    self.bottom_i = self.min_low_i
                    self.last_depth = self.min_low_i - self.top_i
                    self.max_high = high
                    self.max_high_i = self.data_i
        else:
            self.decision_term = 0

    def __depth_bias(self):
        """
        15分足と15秒足に変換
        """
        self.last_depth *= self.FETCH_TERM * self.CANDLESTICK
        self.depth *= self.FETCH_TERM * self.CANDLESTICK

    @staticmethod
    def __and_gate(*args):
        return all(args)

    def make_price_data_frame(self):
        """
        直近のロウソク足データ(2日分)から終値のデータフレームを作る
        :return: pandas.DataFrame 2日分のロウソク足データ
        """
        today = datetime.datetime.now(timezone('UTC'))
        yesterday = today - datetime.timedelta(days=1)
        today = today.astimezone(timezone('Asia/Tokyo'))
        yesterday = yesterday.astimezone(timezone('Asia/Tokyo'))
        print('Initializing Candlestick Data From',
              today.strftime('%Y-%m-%d'),
              'and',
              yesterday.strftime('%Y-%m-%d')
              )
        candlestick_today = self.__api_gateway.use_candlestick(
            time=today.strftime("%Y%m%d"),
            candle_type=self.__candle_type,
            pair=self.__pair
        )['candlestick'][0]['ohlcv']
        candlestick_yesterday = self.__api_gateway.use_candlestick(
            time=yesterday.strftime('%Y%m%d'),
            candle_type=self.__candle_type,
            pair=self.__pair
        )['candlestick'][0]['ohlcv']
        for item in candlestick_today:
            candlestick_yesterday.append(item)
        return pd.DataFrame(candlestick_yesterday, columns=['open', 'high', 'low', 'end', 'yield', 'time'])

    def set_genome(self, genome):
        self.genome = genome
        self.depth = genome[0]
        self.buy_deviation = genome[1]
        self.sell_deviation = genome[2]
        # 設定
        self.genome = [10, 0.02, 0.02]
        self.depth = genome[0]
        self.buy_deviation = genome[1]
        self.sell_deviation = genome[2]
        self.rsi_term = 14
        self.rsi_bottom = 35.0
