import numpy as np


def simple_moving_average(data, term):
    """
    dataの時系列で新しい順に（後ろから）termの期間の単純移動平均線を返す関数
    :param data: array like 時系列順のデータ
    :param term: int   期間
    :return:     numpy 単純移動平均線のリスト
    """
    average_list = list()
    start = term - 1
    for i in range(len(data) - start):
        # numpy[start:stop:steps] stopは含まれない
        values = data[i:i + start + 1]
        average_list.append(float(np.sum(values) / term))
    return np.asarray(a=average_list, dtype=np.float32)


def standard_deviation(data, term):
    """
    dataの時系列で新しい順に（後ろから）termの期間の標準偏差を返す関数
    :param data: numpy データ(単純移動平均のリスト)
    :param term: int   期間
    :return:     numpy 標準偏差のリスト
    """
    std_list = list()
    start = term - 1
    for i in range(len(data) - start):
        # numpy[start:stop:steps] stopは含まれない
        values = data[i:i + start + 1]
        std_list.append(np.std(a=values))
    return np.asarray(a=std_list, dtype=np.float32)


def volatility(sma, std):
    """
    引き数のデータ長の単純移動平均線の標準偏差を計算して、
    上部バンド、下部バンドを返す関数
    :param sma:  float 単純移動平均の値
    :param std:  float 標準偏差
    :return:     dict  ボラティリティ
    """
    volatility_dict = dict()
    volatility_dict['double_upper'] = sma + 2 * std
    volatility_dict['upper'] = sma + std
    volatility_dict['sma'] = sma
    volatility_dict['lower'] = sma - std
    volatility_dict['double_lower'] = sma - 2 * std
    return volatility_dict


def linear_regression(x, t, basic_function):
    """
    線形回帰 正則化なし
    :param   x:              numpy  入力値
    :param   t:              numpy  目標値
    :param   basic_function: object 基底関数を算出するクラスオブジェクト
    :return: w:              numpy  重みパラメータ
    """
    phi_x = basic_function(x)
    tmp = np.linalg.inv(np.dot(phi_x.T, phi_x))
    w = np.dot(np.dot(tmp, phi_x.T), t)
    return w


class Polynomial(object):
    """
    多項式の基底関数
    """
    def __init__(self, dim=1):
        """
        :param dim: int 多項式の次元 (初期値は0次元なので、入力値のまま)
        """
        self._dim = dim

    def __call__(self, x):
        return np.array([x ** i for i in range(self._dim)]).T
