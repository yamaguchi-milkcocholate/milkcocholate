from modules.datamanager.macd import MACD
from modules.db.writer import Writer
import pickle


class MACDTrader:
    """
    MACDの取引を想定
    """
    PLUS = 1
    MINUS = -1
    BUY = 1
    SELL = 2
    STAY = 3
    DEFAULT_YEN_POSITION = 1000
    LOSS_CUT_RATE = 1

    def __init__(self, short_term=12, long_term=26, signal=9, is_exist_pickle=False):
        """
        :param short_term:
        :param long_term:
        :param signal:
        """
        self.__genome = None
        self.__candlestick = None
        self.trend_15min = None
        self.trend_5min = None
        self.area_15min = None
        self.area_5min = None
        self.max_histogram_5min = None
        self.max_histogram_15min = None
        self.start_macd_15min = None
        self.start_macd_5min = None
        self.start_signal_15min = None
        self.start_signal_5min = None
        self.__short_term = short_term
        self.__long_term = long_term
        self.__signal = signal
        self.__is_exist_pickle = is_exist_pickle
        self.__macd = MACD(
            use_of_data='validation'
        )
        self.data = self.__macd(
            short_term=self.__short_term,
            long_term=self.__long_term,
            signal=self.__signal,
            is_pickle=self.__is_exist_pickle,
            is_validation=False
        )

    def __call__(self, *args, **kwargs):
        self.trend_15min = self.PLUS
        self.trend_5min = self.PLUS
        self.area_15min = list()
        self.area_5min = list()
        self.max_histogram_5min = 0
        self.max_histogram_15min = 0
        self.start_macd_15min = 0
        self.start_macd_5min = 0
        self.start_signal_15min = 0
        self.start_signal_5min = 0
        coin = 0
        has_coin = False
        loss_cut = 0
        loss = 0
        total = 0
        transaction = 0
        buying_price = None
        for data_i in range(len(self.data)):
            price = self.data.loc[data_i].price

            operation = self.operation(
                data_i=data_i,
                has_coin=has_coin,
            )
            if has_coin:
                print(price)

            if self.BUY == operation:
                coin = self.DEFAULT_YEN_POSITION / price
                has_coin = True
                buying_price = price
            elif self.SELL == operation:
                benefit = price * coin - self.DEFAULT_YEN_POSITION
                coin = 0
                has_coin = False
                transaction += 1
                if benefit > 0:
                    total += benefit
                else:
                    loss += benefit
                print(benefit, '利益:', total, '損失:', loss, '価格:', buying_price, '→', price)
            # 損切り
            if buying_price and price < (buying_price * self.LOSS_CUT_RATE) and has_coin is True:
                loss_cut += 1
                benefit = price * coin - self.DEFAULT_YEN_POSITION
                if benefit > 0:
                    total += benefit
                else:
                    loss += benefit
                print('損切り:', '開始価格:', buying_price, '現在価格:', price)
                coin = 0
                has_coin = False
                buying_price = None
        print('終了:', '合計:', (total + loss), '損切り:', loss_cut)
        print(self.__genome)

    def operation(self, data_i, has_coin):
        histogram_15min = float(self.data.loc[data_i].histogram_15min)
        histogram_1min = float(self.data.loc[data_i].histogram_5min)
        pre_trend_15min = self.trend_15min
        pre_trend_5min = self.trend_5min
        macd_15min = float(self.data.loc[data_i].macd_15min)
        macd_5min = float(self.data.loc[data_i].macd_5min)
        signal_15min = float(self.data.loc[data_i].signal_15min)
        signal_5min = float(self.data.loc[data_i].signal_5min)
        if histogram_15min >= 0:
            self.trend_15min = self.PLUS
        elif histogram_15min < 0:
            self.trend_15min = self.MINUS
        if histogram_1min >= 0:
            self.trend_5min = self.PLUS
        elif histogram_1min < 0:
            self.trend_5min = self.MINUS

        if pre_trend_15min == self.trend_15min:
            self.area_15min.append(histogram_15min)
            if abs(self.max_histogram_15min) < abs(histogram_15min):
                self.max_histogram_15min = histogram_15min
        else:
            self.area_15min = list()
            self.area_15min.append(histogram_15min)
            self.max_histogram_15min = histogram_15min
            self.start_macd_15min = macd_15min
            self.start_signal_15min = signal_15min
        if pre_trend_5min == self.trend_5min:
            self.area_5min.append(histogram_1min)
            if abs(self.max_histogram_5min) < abs(histogram_1min):
                self.max_histogram_5min = histogram_1min
        else:
            self.area_5min = list()
            self.area_5min.append(histogram_1min)
            self.max_histogram_5min = histogram_1min
            self.start_macd_5min = macd_5min
            self.start_signal_5min = signal_5min

        # 山が下がり始めたら
        if len(self.area_5min) > 1 and self.is_exceed(abs(self.area_5min[-1]), abs(self.area_5min[-2])):
            step_size_5min = len(self.area_5min)
            start_decrease_5min = True
        else:
            step_size_5min = None
            start_decrease_5min = False
        if len(self.area_15min) > 1 and self.is_exceed(abs(self.area_15min[-1]), abs(self.area_15min[-2])):
            step_size_15min = len(self.area_15min)
            start_decrease_15min = True
        else:
            step_size_15min = None
            start_decrease_15min = False

        if start_decrease_5min and start_decrease_15min:

            # 買い
            if has_coin is False:
                decrease_rate_15min = self.__genome[0]
                step_rate_15min = self.__genome[1]
                decrease_rate_5min = self.__genome[2]
                step_rate_5min = self.__genome[3]
                start_macd_15min = self.__genome[4]
                start_signal_15min = self.__genome[5]
                start_macd_5min = self.__genome[6]
                start_signal_5min = self.__genome[7]
                end_macd_15min = self.__genome[8]
                end_signal_15min = self.__genome[9]
                end_macd_5min = self.__genome[10]
                end_signal_5min = self.__genome[11]
                # MAX条件
                max_threshold_5min = (step_rate_5min ** 2) * self.max_histogram_5min
                max_threshold_5min += start_macd_5min * self.start_macd_5min
                max_threshold_5min += start_signal_5min * self.start_signal_5min
                max_threshold_5min += end_macd_5min * macd_5min
                max_threshold_5min += end_signal_5min * signal_5min
                max_threshold_15min = (step_rate_15min ** 2) * self.max_histogram_15min
                max_threshold_15min += start_macd_15min * self.start_macd_15min
                max_threshold_15min += start_signal_15min * self.start_signal_15min
                max_threshold_15min += end_macd_15min * macd_15min
                max_threshold_15min += end_signal_15min * signal_15min
                # 降下条件
                decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min
                decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min

                buy = self.and_gate(
                    self.is_exceed(self.max_histogram_15min, max_threshold_15min),
                    self.is_exceed(decrease_threshold_15min, histogram_15min),
                    self.is_exceed(self.max_histogram_5min, max_threshold_5min),
                    self.is_exceed(decrease_threshold_5min, histogram_1min),
                )
                if buy:
                    operation = self.BUY
                else:
                    operation = self.STAY
            # 売り
            elif has_coin is True:
                decrease_rate_15min = self.__genome[12]
                step_rate_15min = self.__genome[13]
                decrease_rate_5min = self.__genome[14]
                step_rate_5min = self.__genome[15]
                start_macd_5min = self.__genome[16]
                start_signal_5min = self.__genome[17]
                start_macd_15min = self.__genome[18]
                start_signal_15min = self.__genome[19]
                end_macd_5min = self.__genome[16]
                end_signal_5min = self.__genome[17]
                end_macd_15min = self.__genome[18]
                end_signal_15min = self.__genome[19]
                # MAX条件
                max_threshold_5min = step_rate_5min * step_size_5min * self.max_histogram_5min
                max_threshold_5min += start_macd_5min * self.start_macd_5min
                max_threshold_5min += start_signal_5min * self.start_signal_5min
                max_threshold_5min += end_macd_5min * macd_5min
                max_threshold_5min += end_signal_5min * signal_5min
                max_threshold_15min = step_rate_15min * step_size_15min * self.max_histogram_15min
                max_threshold_15min += start_macd_15min * self.start_macd_15min
                max_threshold_15min += start_signal_15min * self.start_signal_15min
                max_threshold_15min += end_macd_15min * macd_15min
                max_threshold_15min += end_signal_15min * signal_15min
                # 降下条件
                decrease_threshold_5min = self.max_histogram_5min * decrease_rate_5min
                decrease_threshold_15min = self.max_histogram_15min * decrease_rate_15min

                sell = self.and_gate(
                    self.is_exceed(max_threshold_15min, self.max_histogram_15min),
                    self.is_exceed(histogram_15min, decrease_threshold_15min),
                    self.is_exceed(max_threshold_5min, self.max_histogram_5min),
                    self.is_exceed(histogram_1min, decrease_threshold_5min),
                )

                if sell:
                    operation = self.SELL
                else:
                    operation = self.STAY
            else:
                operation = self.STAY
        else:
            operation = self.STAY

        return operation

    def set_genome(self, host, population_id, individual_num=0):
        """
        :param host:
        :param population_id:
        :param individual_num: int 個体の番号、初期値は0番のエリート
        """
        population = Writer(host=host).find(
            table='populations',
            search_id=population_id
        )[0]
        genomes = pickle.loads(population['genome'])
        # 個体を選ぶ
        if individual_num >= len(genomes):
            raise TypeError('no individual number')
        self.__genome = genomes[individual_num]

    @staticmethod
    def is_exceed(x, y):
        """
        :param x: 小さい
        :param y: 大きい
        :return: bool
        """
        if y > x:
            return True
        else:
            return False

    @staticmethod
    def and_gate(*args):
        return all(args)
