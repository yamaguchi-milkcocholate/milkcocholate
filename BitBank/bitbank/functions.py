import numpy as np


def cosine_similarity(x, y):
    """
    コサイン類似度
    :param x: numpy
    :param y: numpy
    :return: float
    """
    x_size = np.sqrt(np.sum(x * x))
    y_size = np.sqrt(np.sum(y * y))
    product = np.sum(x * y)
    return product / x_size / y_size


def wave_template(wave_id, size):
    """
    波形テンプレート
    :param wave_id:
    :param size:
    :return: numpy
    """
    # 1円の下落
    if wave_id == 1:
        pass
    elif wave_id == 2:
        pass


def line(length, inclination, bias):
    """
    直線を引く
    :param length: integer
    :param inclination: number
    :param bias: number
    :return: numpy
    """
    return np.arange(0, length) * inclination + bias
