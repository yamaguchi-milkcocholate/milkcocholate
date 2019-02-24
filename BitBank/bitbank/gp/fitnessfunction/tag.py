from bitbank.gp.fitnessfunction.fitnessfunction import FitnessFunction
from bitbank.functions import load_data
from bitbank.adviser.functions import *
import math


class TagFitnessFunction(FitnessFunction):

    def __init__(self, ema_term, ma_term, goal):
        super().__init__()
        self.ema_term = ema_term
        self.ma_term = ma_term
        self.goal = goal
        self.candlestick = load_data('15min', 'data_xrp')
        self.data = None
        self.ranges = dict()
        self.make_data_frame()
        self.feature_range()

    def calc_fitness(self, genomes):
        """
        全ての遺伝子の適応度を計算
        :param genomes:
        :return:
        """
        fitness = list()
        for genome_i in range(len(genomes)):
            fitness.append(self.simulate(genome=genomes[genome_i], data_size=len(self.data)))
        return np.asarray(fitness)

    def simulate(self, genome, data_size):
        """
        ある遺伝子についてシミュレーションする
        :param genome:
        :param data_size:
        :return:
        """
        is_check = False
        buying_price = None
        success = 0
        fail = 0
        # PRICE > MA, PRICE > EMAになったらTrue
        is_second = None
        for data_i in range(self.ma_term, data_size):
            ema_price_diff = self.ema_price_diff(data_i=data_i)
            ema_ma_diff = self.ema_ma_diff(data_i=data_i)
            # 売りのタイミングを探る
            if is_check:
                is_check, success, fail, buying_price, is_second = self.__buy_judge(
                    data_i,
                    buying_price,
                    is_second,
                    success,
                    fail
                )
            else:
                inc, e = self.ma_regression(data_i=data_i)
                ma_diff = self.ma_diff(data_i=data_i)
                r = genome.operation(
                    inc=inc,
                    e=e,
                    ema_price_diff=ema_price_diff,
                    ema_ma_diff=ema_ma_diff,
                    ma_diff=ma_diff
                )
                if r:
                    is_check = True
                    buying_price = self.price(data_i=data_i)
                    is_second = False
        fitness = self.__fitness(success=success, fail=fail)
        print('{:>5}'.format(success) + '/{:<5}'.format(success + fail) + '  {:.3f}'.format(success / (success + fail)) + '  {:.5f}'.format(fitness))
        return fitness

    @staticmethod
    def __fitness(success, fail):
        """
        適応度を計算
        試行回数に重みをつける
        少ない時に罰則
        ロジスティック関数
        :param success:
        :param fail:
        :return:
        """
        trial = success + fail + 1
        w = (100 * math.exp(trial * 0.08)) / (100 + math.exp(trial * 0.08))
        return 1 / 1000 * math.exp(10 * (success / trial)) * w

    def __buy_judge(self, data_i, buying_price, is_second, success, fail):
        """
        買いオペレーションが成功したかどうか
        :param data_i:
        :param buying_price:
        :param is_second:
        :param success:
        :param fail:
        :return:
        """
        price = float(self.data.loc[data_i, 'high'])
        ma = float(self.data.loc[data_i, 'ma'])
        ema = float(self.data.loc[data_i, 'ema'])

        # すでに一度,PRICE > MA, PRICE > EMAになっている
        if is_second:
            # 成功
            if (price > ma) and (price > ema) and (price > self.goal + buying_price):
                return False, success + 1, fail, None, None
            # 失敗
            elif price < ma:
                return False, success, fail + 1, None, None
            # 審議中
            else:
                return True, success, fail, buying_price, True
        else:
            # 審議中(PRICE > MA, PRICE > EMAになった)
            if (price > ma) and (price > ema):
                # 一気に成功した時
                if price > self.goal + buying_price:
                    return False, success + 1, fail, None, None
                else:
                    return True, success, fail, buying_price, True
            # 審議中(PRICE > MA, PRICE > EMAになってない)
            else:
                return True, success, fail, buying_price, False

    def feature_range(self):
        data_size = len(self.data)
        inc_list = list()
        e_list = list()
        ema_price_diff_list = list()
        ema_ma_diff_list = list()
        ma_diff_list = list()
        for data_i in range(self.ma_term, data_size):
            inc, e = self.ma_regression(data_i=data_i)
            ema_price_diff = self.ema_price_diff(data_i=data_i)
            ema_ma_diff = self.ema_ma_diff(data_i=data_i)
            ma_diff = self.ma_diff(data_i=data_i)
            inc_list.append(inc)
            e_list.append(e)
            ema_price_diff_list.append(ema_price_diff)
            ema_ma_diff_list.append(ema_ma_diff)
            ma_diff_list.append(ma_diff)

        self.__stats(name='inc', d_list=inc_list)
        self.__stats(name='e', d_list=e_list)
        self.__stats(name='ema_price_diff', d_list=ema_price_diff_list)
        self.__stats(name='ema_ma_diff', d_list=ema_ma_diff_list)
        self.__stats(name='ma_diff', d_list=ma_diff_list)

    def __stats(self, name, d_list):
        print(name, end='')
        d_min = min(d_list)
        d_max = max(d_list)
        d_ave = sum(d_list) / len(d_list)
        for i in range(20 - len(name)):
            print(' ', end='')
        print(': {0:.8f}'.format(min(d_list)) + ' ~ {0:.8f}'.format(max(d_list)) + '  ave.{0:8f}'.format(d_ave))
        self.ranges[name] = {'min': d_min, 'max': d_max, 'ave': d_ave}
        self.condition.add_technical_analysis(
            name=name,
            lower_limit=d_min,
            upper_limit=d_max
        )

    def make_data_frame(self):
        """
        MAとEMAを付け加える
        """
        ends = self.candlestick.end.values
        ma = simple_moving_average(data=ends, term=self.ma_term)
        ema = exponential_moving_average(data=ends, term=self.ema_term)
        if len(ema) > len(ma):
            r_len = len(ma)
        else:
            r_len = len(ema)
        self.candlestick, ma, ema = self.__uniform_length(self.candlestick, ma, ema, r_len)
        self.data = self.candlestick
        self.data['ma'] = ma
        self.data['ema'] = ema
        self.data = self.data.reset_index(drop=True)

    def price(self, data_i):
        return float(self.data.loc[data_i, 'end'])

    def ma_regression(self, data_i):
        """
        MAの線形回帰と二乗和誤差
        :param data_i:
        :return:
        """
        ma_list = self.data.loc[data_i - self.ma_term:data_i-1].ma.values
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(ma_list))
        w = linear_regression(x=x, t=ma_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - ma_list
        e = e * e.T
        e = np.sum(e)
        return w[1], e

    def ema_price_diff(self, data_i):
        """
        PRICEとEMAの乖離
        :param data_i:
        :return:
        """
        return float(self.data.loc[data_i, 'ema']) - float(self.data.loc[data_i, 'end'])

    def ema_ma_diff(self, data_i):
        """
        MAとEMAの乖離
        :param data_i:
        :return:
        """
        return float(self.data.loc[data_i, 'ema']) - float(self.data.loc[data_i, 'ma'])

    def ma_diff(self, data_i):
        """
        MAの直前の傾き
        :param data_i:
        :return:
        """
        return float(self.data.loc[data_i, 'ma']) - float(self.data.loc[data_i - 1, 'ma'])

    @staticmethod
    def __uniform_length(candlestick, ma, ema, r_len):
        candlestick = candlestick.loc[len(candlestick) - r_len:]
        ma = ma[len(ma) - r_len:]
        ema = ema[len(ema) - r_len:]
        return candlestick, ma, ema

    def get_data(self):
        return self.data

    def get_ranges(self):
        return self.ranges

    def get_condition(self):
        return self.condition
