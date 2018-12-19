import numpy as np
import matplotlib.pyplot as plt
import math

PATTERN = 9
INC = 1


def show_wave(**kwargs):
    """
    非線形データをプロットする関数
    :param kwargs: numpy[]
    """
    size = len(kwargs)
    if size % 2 == 0:
        size = len(kwargs) / 2
    else:
        size = len(kwargs) / 2 + 1

    for i, key in enumerate(kwargs):
        plt.subplot(size, 2, i + 1)
        # plot
        plt.plot(kwargs[key], marker='.', label=key)
        plt.legend()
    plt.show()


def diff(data):
    """
    差分を返す関数
    :param data: numpy
    :return: numpy
    """
    tmp = data[:-1]
    data = data[1:]
    data = data - tmp
    return data


def template(size, number):
    if size % 2 == 0:
        size += 1

    if number is 0:
        data = np.zeros(size)
        return data
    elif number is 1:
        data = np.arange(-1 * size / 2, size / 2)
        data = data * INC
        return data
    elif number is 2:
        data = np.arange(-1 * size / 2, size / 2)
        data = -1 * data * INC
        return data
    elif number is 3:
        # 前半の右肩上がり
        data = np.arange(-1 * size / 2, 0)
        data = data - np.average(data)
        data = data * INC
        tmp = np.zeros_like(data)[:-1]
        tmp = tmp + data[-1]
        data = np.append(data, tmp)
        return data
    elif number is 4:
        # 後半の右肩下がり
        data = np.arange(0, size / 2)
        data = data - np.average(data)
        data = -1 * data * INC
        tmp = np.zeros_like(data)[:-1]
        tmp = tmp + data[0]
        data = np.append(tmp, data)
        return data
    elif number is 5:
        # 前半右肩下がり
        data = np.arange(0, size / 2)
        data = data - np.average(data)
        data = -1 * data * INC
        tmp = np.zeros_like(data)[:-1]
        tmp = tmp + data[-1]
        data = np.append(data, tmp)
        return data
    elif number is 6:
        # 前半の右肩上がり
        data = np.arange(-1 * size / 2, 0)
        data = data - np.average(data)
        data = data * INC
        tmp = np.zeros_like(data)[:-1]
        tmp = tmp + data[0]
        data = np.append(tmp, data)
        return data
    elif number is 7:
        # 上に凸
        data = np.arange(-1 * size / 2, 0)
        data = data - np.average(data)
        data = data * INC
        tmp = np.arange(0, size / 2)
        tmp = tmp - np.average(tmp)
        tmp = -1 * tmp * INC
        data = np.append(data, tmp[1:])
        return data
    elif number is 8:
        # 下に凸
        data = np.arange(-1 * size / 2, 0)
        data = data - np.average(data)
        data = data * INC
        tmp = np.arange(0, size / 2)
        tmp = tmp - np.average(tmp)
        tmp = -1 * tmp * INC
        data = np.append(tmp, data[:-1])
        return data


def normalize(data):
    tmp = data * data
    tmp = np.sum(tmp)
    # 原点ベクトルはそのまま返す
    if tmp == 0:
        return data
    tmp = math.sqrt(tmp)
    data = data / tmp
    return data


def cosine_similarity(x, y):
    """
    コサイン類似度を返す関数
    :param x: numpy
    :param y: numpy
    :return: numpy | float
    """
    if len(x) != len(y):
        raise Exception()

    x_norm = np.linalg.norm(x)
    y_norm = np.linalg.norm(y)
    sim = np.sum(x * y)
    sim = sim / (x_norm * y_norm + 0.00000000001)
    return sim


def correlation_coefficient(x, y):
    """
    ピアソン相関係数
    :param x: numpy
    :param y: numpy
    :return: numpy
    """
    if len(x) != len(y):
        print(x)
        print(y)
        raise Exception()

    x = x - np.average(x)
    y = y - np.average(y)
    return cosine_similarity(x, y)


def deviation_pattern_similarity(x, y):
    """
    偏差パターン類似度
    :param x: numpy
    :param y: numpy
    :return: numpy
    """
    if len(x) != len(y):
        raise Exception()

    m = x + y / 2
    x = x - m
    y = y - m
    return cosine_similarity(x, y)


def pattern_analysis(x):
    """
    パターン分けする関数
    :param x: numpy
    :return: integer
    """
    size = len(x)
    sim = list()
    if size % 2 == 0:
        raise Exception()

    for i in range(PATTERN):
        tpl = template(size=size, number=i)
        sim.append(correlation_coefficient(tpl, x))
        print('pattern', i, ':', sim[-1])
    return sim.index(max(sim))
