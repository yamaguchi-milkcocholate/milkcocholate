from bitbank.gp.fitnessfunction.fitnessfunction import FitnessFunction
from bitbank.functions import load_data
from bitbank.adviser.functions import *
import math


class TagNextFitnessFunction(FitnessFunction):

    def __init__(self, ema_term, ma_term, goal, buy_genome, limit, data, top, balance, edge):
        super().__init__()
        self.ema_term = ema_term
        self.ma_term = ma_term
        self.goal = goal
        self.buy_genome = buy_genome
        self.limit = limit
        self.top = top
        self.balance = balance
        self.edge = edge
        self.candlestick = load_data(data, 'data_xrp')
        self.data = None
        self.ranges = dict()
        self.tech_data = dict()
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
        s = 0
        f = 0
        count = 0
        # PRICE > MA, PRICE > EMAになったらTrue
        for data_i in range(self.ma_term, data_size):
            ema_price_diff = self.tech_data[data_i]['ema_price_diff']
            ema_ma_diff = self.tech_data[data_i]['ema_ma_diff']
            inc = self.tech_data[data_i]['inc']
            e = self.tech_data[data_i]['e']
            ma_diff = self.tech_data[data_i]['ma_diff']
            ema_inc = self.tech_data[data_i]['ema_inc']
            ema_e = self.tech_data[data_i]['ema_e']
            ema_diff = self.tech_data[data_i]['ema_diff']
            price = self.tech_data[data_i]['price']
            price_inc = self.tech_data[data_i]['price_inc']
            price_e = self.tech_data[data_i]['price_e']
            # 売りのタイミングを探る
            if is_check:
                count += 1
                r = genome.operation(
                    inc=inc,
                    e=e,
                    ema_price_diff=ema_price_diff,
                    ema_ma_diff=ema_ma_diff,
                    ma_diff=ma_diff,
                    price=price - buying_price,
                    ema_inc=ema_inc,
                    ema_e=ema_e,
                    ema_diff=ema_diff,
                    price_inc=price_inc,
                    price_e=price_e
                )
                if r:
                    success, fail, s, f = self.__sell_judge(
                        buying_price,
                        success,
                        fail,
                        price,
                        s,
                        f
                    )
                    is_check = False
                    buying_price = None
                    count = 0
                if count >= self.limit:
                    fail += 1
                    is_check = False
                    buying_price = None
                    count = 0
            # 買いのタイミングを探る
            else:
                r = self.buy_genome.operation(
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
                if r:
                    is_check = True
                    buying_price = self.price(data_i=data_i)
        fitness = self.__fitness(success=success, fail=fail, s=s, f=f)
        if s + f > 0:
            r = s / (s + f)
        else:
            r = 0
        if success + fail > 0:
            rate = success / (success + fail)
        else:
            rate = 0
        print('{:>5}'.format(s) + '/{:<5}'.format(s + f) + '  {:.3f}'.format(r) + '  {:.5f}'.format(rate) + '  {:.5f}'.format(
            fitness))
        return fitness

    def __sell_judge(self, buying_price, success, fail, price, s, f):
        if buying_price + self.goal <= price:
            return success + 10, fail, s + 1, f
        # elif buying_price > price:
            # return success + 1, fail, s + 1, f
        else:
            return success, fail + 10, s, f + 1

    def __fitness(self, success, fail, s, f):
        """
        適応度を計算
        試行回数に重みをつける
        少ない時に罰則
        ロジスティック関数
        :param success:
        :param fail:
        :return:
        """
        edge = s + f
        if edge >= self.edge:
            fitness = (self.balance / self.edge) * success + ((self.balance - self.top) / self.edge) * fail + (self.top - self.balance)
        else:
            fitness = (self.top / self.edge) * success
        if fitness <= 0:
            fitness = 0
        return fitness + 1

    def feature_range(self):
        data_size = len(self.data)
        inc_list = list()
        e_list = list()
        ema_price_diff_list = list()
        ema_ma_diff_list = list()
        ma_diff_list = list()
        ema_diff_list = list()
        ema_inc_list = list()
        ema_e_list = list()
        price_list = list()
        price_inc_list = list()
        price_e_list = list()
        for data_i in range(self.ma_term, data_size):
            inc, e = self.ma_regression(data_i=data_i)
            ema_price_diff = self.ema_price_diff(data_i=data_i)
            ema_ma_diff = self.ema_ma_diff(data_i=data_i)
            ma_diff = self.ma_diff(data_i=data_i)
            ema_diff = self.ema_diff(data_i=data_i)
            ema_inc, ema_e = self.ema_regression(data_i=data_i)
            price_inc, price_e = self.price_regression(data_i=data_i)

            inc_list.append(inc)
            e_list.append(e)
            ema_price_diff_list.append(ema_price_diff)
            ema_ma_diff_list.append(ema_ma_diff)
            ma_diff_list.append(ma_diff)
            ema_diff_list.append(ema_diff)
            ema_inc_list.append(ema_inc)
            ema_e_list.append(ema_e)
            price_inc_list.append(price_inc)
            price_e_list.append(price_e)
            price_list.append(self.price(data_i))
            add = {
                'inc': inc, 'e': e, 'ema_price_diff': ema_price_diff, 'ema_ma_diff': ema_ma_diff, 'ma_diff': ma_diff,
                'ema_diff': ema_diff, 'ema_inc': ema_inc, 'ema_e': ema_e, 'price': self.price(data_i), 'price_inc': price_inc, 'price_e': price_e
            }
            self.tech_data[data_i] = add
        min_list = [min(price_list)] * len(price_list)

        def norm(x, m):
            return x - m
        price_list = list(map(norm, price_list, min_list))

        self.__stats(name='inc', d_list=inc_list)
        self.__stats(name='e', d_list=e_list)
        self.__stats(name='ema_price_diff', d_list=ema_price_diff_list)
        self.__stats(name='ema_ma_diff', d_list=ema_ma_diff_list)
        self.__stats(name='ma_diff', d_list=ma_diff_list)
        self.__stats(name='ema_inc', d_list=ema_inc_list)
        self.__stats(name='ema_e', d_list=ema_e_list)
        self.__stats(name='ema_diff', d_list=ema_diff_list)
        self.__stats(name='price', d_list=price_list)
        self.__stats(name='price_inc', d_list=price_inc_list)
        self.__stats(name='price_e', d_list=price_e_list)

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

    def price_regression(self, data_i):
        ema_list = self.data.loc[data_i - self.ma_term:data_i - 1].end.values
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(ema_list))
        w = linear_regression(x=x, t=ema_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - ema_list
        e = e * e.T
        e = np.sum(e)
        return w[1], e

    def ema_regression(self, data_i):
        ema_list = self.data.loc[data_i - self.ema_term:data_i - 1].ema.values
        poly = Polynomial(dim=2)
        x = np.arange(start=0, stop=len(ema_list))
        w = linear_regression(x=x, t=ema_list, basic_function=poly)
        poly.set_coefficient(w=w)
        reg = np.asarray([poly.func(x=i) for i in range(len(x))])
        e = reg - ema_list
        e = e * e.T
        e = np.sum(e)
        return w[1], e

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

    def ema_diff(self, data_i):
        return float(self.data.loc[data_i, 'ema']) - float(self.data.loc[data_i - 1, 'ema'])

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
