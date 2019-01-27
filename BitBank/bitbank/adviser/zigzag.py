from bitbank.apigateway import ApiGateway
import pandas as pd
from pytz import timezone
import datetime
from bitbank.line import Line


class ZigZagAdviser:
    BUY = 1
    STAY = 2
    SELL = 3

    TOP = 10   # 値幅率を超えて上がっているときの状態
    BOTTOM = 11   # 値幅率を超えて下がっているときの状態
    OTHER = 12

    TOP_DECISION_TERM = 60   #
    BOTTOM_DECISION_TERM = 150   #

    FETCH_TERM = 4  # 4 /min
    CANDLESTICK = 15  # 15min

    def __init__(self, pair='xrp_jpy', candle_type='15min', buying_price=None, limit=None, init_max_high=None, init_min_low=None):
        self.__pair = pair
        self.__candle_type = candle_type
        self.__api_gateway = ApiGateway()
        self.genome = None
        self.buy_deviation = None
        self.sell_deviation = None
        self.rsi_term = None
        self.rsi_data = None
        self.rsi_step = None
        self.rsi_bottom = None
        self.rsi_top = None
        self.max_high = None
        self.min_low = None
        self.price = None
        self.trend = None
        self.__line = Line()
        self.buying_price = buying_price
        self.limit = limit
        self.decision_term = 0
        self.candlestick = self.make_price_data_frame()
        self.init_max_high = init_max_high
        self.init_min_low = init_min_low

    def __call__(self):
        self.is_candlestick = True
        self.zigzag_candlestick()
        self.is_candlestick = False
        self.candlestick = None
        # 初期値
        if self.init_max_high is not None:
            self.max_high = self.init_max_high
        if self.init_min_low is not None:
            self.min_low = self.init_min_low

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
        if price is None:
            price = self.__api_gateway.use_ticker(pair=self.__pair)
            price = float(price['last'])

        self.__update_min_max(high=price, low=price)
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

        for data_i in range(1, len(self.candlestick)):
            high = float(self.candlestick.loc[data_i].high)
            low = float(self.candlestick.loc[data_i].low)

            self.__update_min_max(high=high, low=low)

            self.__trend(high=high, low=low)

        # RSI
        self.rsi_data = list()
        for data_i in range(len(self.candlestick) - self.rsi_term, len(self.candlestick)):
            self.rsi_data.append({
                'start': float(self.candlestick.loc[data_i].open),
                'end': float(self.candlestick.loc[data_i].end)
            })
        self.rsi_step = 0

    def rsi(self):
        plus = list()
        minus = list()
        for data in self.rsi_data:
            diff = data['end'] - data['start']
            if diff > 0:
                plus.append(diff)
            else:
                minus.append(-1 * diff)
        if len(plus) > 0:
            plus_sum = sum(plus)
        else:
            plus_sum = 0
        if len(minus) > 0:
            minus_sum = sum(minus)
        else:
            minus_sum = 0
        return plus_sum / (plus_sum + minus_sum) * 100

    def __update_min_max(self, high, low):
        if self.max_high < high:
            self.max_high = high
        if self.min_low > low:
            self.min_low = low

    def __top(self):
        """
        値幅率を超えて上がったときにTrue
        :return:
        """
        if self.price is None:
            price = self.max_high
        else:
            price = self.price
        if self.buying_price is None or self.is_candlestick:
            return self.__and_gate(
                self.min_low * (1 + self.sell_deviation) < price,
            )
        else:
            return self.__and_gate(
                self.min_low * (1 + self.sell_deviation) < price,
                self.buying_price <= self.price
            )

    def __bottom(self):
        """
        値幅率を超えて下がったときにTrue
        :return:
        """
        if self.price is None:
            price = self.min_low
        else:
            price = self.price
        if self.limit is None or self.is_candlestick:
            return self.__and_gate(
                self.max_high * (1 - self.buy_deviation) > price,
            )
        else:
            return self.__and_gate(
                self.max_high * (1 - self.buy_deviation) > price,
                self.limit >= self.price
            )

    def __trend(self, high=None, low=None):
        if high is None:
            high = self.price
        if low is None:
            low = self.price

        self.trend = self.OTHER

        if not self.is_candlestick:
            print(self.min_low, self.price, self.max_high)

        if self.__top():
            # 最大値更新
            if high >= self.max_high:
                self.decision_term = 0
                if not self.is_candlestick:
                    self.__line(message="最大値を更新")
            else:
                self.decision_term += 1
                if not self.is_candlestick:
                    rsi = self.rsi()
                    self.__deliberating_message(side='sell', rsi=rsi)
                else:
                    rsi = True
                # 山を決定
                if self.is_candlestick or (self.decision_term >= self.TOP_DECISION_TERM and self.rsi_top <= rsi):
                    self.decision_term = 0
                    self.trend = self.TOP
                    self.min_low = low
                    print('TOP')

        elif self.__bottom():
            # 最小値更新
            if low <= self.min_low:
                self.decision_term = 0
                if not self.is_candlestick:
                    self.__line(message="最小値を更新")
            else:
                self.decision_term += 1
                # 谷を決定
                if not self.is_candlestick:
                    rsi = self.rsi()
                    self.__deliberating_message(side='buy', rsi=rsi)
                else:
                    rsi = True
                if self.is_candlestick or (self.decision_term >= self.BOTTOM_DECISION_TERM and self.rsi_bottom >= rsi):
                    self.decision_term = 0
                    self.trend = self.BOTTOM
                    self.max_high = high
                    print('BOTTOM')
        else:
            self.decision_term = 0

    def __deliberating_message(self, side, **kwargs):
        if side == 'buy':
            message = "買いエントリーを審議中\n" \
                      "decision : " + str(self.decision_term) + "\n" \
                      "RSI : " + str(kwargs['rsi']) + "\n" \
                      "" + str(self.__now())
        elif side == 'sell':
            message = "売りエントリーを審議中\n" \
                      "decision : " + str(self.decision_term) + "\n" \
                      "RSI : " + str(kwargs['rsi']) + "\n" \
                      "" + str(self.__now())
        else:
            message = ""
        if self.decision_term == 1 or self.decision_term % 10 == 0:
            self.__line(message=message)

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

    @staticmethod
    def __now():
        return datetime.datetime.now(timezone('UTC')).astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')

    def set_genome(self, genome):
        self.genome = genome
        # 設定
        self.genome = [10, 0.018, 0.012]
        self.buy_deviation = self.genome[1]
        self.sell_deviation = self.genome[2]
        self.rsi_term = 14
        self.rsi_bottom = 35.0
        self.rsi_top = 60.0
