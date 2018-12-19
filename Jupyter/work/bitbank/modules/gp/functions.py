import numpy as np
import matplotlib.pyplot as plt


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

    inc = 1

    if number is 0:
        data = np.zeros(size)
        return data
    elif number is 1:
        data = np.arange(-1 * (size / 2), size / 2)
        data = data * inc
        return data
    elif number is 2:
        # 前半の右肩上がり
        data = np.arange(-1 * size / 2, 0)
        data = data - np.average(data)
        data = data * inc
        tmp = np.zeros_like(data)[:-1]
        tmp = tmp + data[-1]
        data = np.append(data, tmp)
        return data
    elif number is 3:
        # 後半の右肩下がり
        data = np.arange(0, size / 2)
        data = data - np.average(data)
        data = -1 * data * inc
        tmp = np.zeros_like(data)[:-1]
        tmp = tmp + data[0]
        data = np.append(tmp, data)
        return data
    elif number is 4:
        # 前半右肩下がり
        data = np.arange(0, size / 2)
        data = data - np.average(data)
        data = -1 * data * inc
        tmp = np.zeros_like(data)[:-1]
        tmp = tmp + data[-1]
        data = np.append(data, tmp)
        return data
    elif number is 5:
        # 前半の右肩上がり
        data = np.arange(-1 * size / 2, 0)
        data = data - np.average(data)
        data = data * inc
        tmp = np.zeros_like(data)[:-1]
        tmp = tmp + data[0]
        data = np.append(tmp, data)
        return data
    elif number is 6:
        # 上に凸
        data = np.arange(-1 * size / 2, 0)
        data = data - np.average(data)
        data = data * inc
        tmp = np.arange(0, size / 2)
        tmp = tmp - np.average(tmp)
        tmp = -1 * tmp * inc
        data = np.append(data, tmp)
        return data
    elif number is 7:
        # 上に凸
        data = np.arange(-1 * size / 2, 0)
        data = data - np.average(data)
        data = data * inc
        tmp = np.arange(0, size / 2)
        tmp = tmp - np.average(tmp)
        tmp = -1 * tmp * inc
        data = np.append(tmp, data)
        return data
