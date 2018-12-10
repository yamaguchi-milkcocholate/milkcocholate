import numpy as np


def simple_moving_average(data, term):
    """
    後ろ順で引き数のデータ長の単純移動平均線を返す関数
    :param data: numpy
    :param term: int
    :return:     numpy
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
    後ろ順で引き数のデータ長の標準偏差を返す
    :param data:
    :param term:
    :return: numpy
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
