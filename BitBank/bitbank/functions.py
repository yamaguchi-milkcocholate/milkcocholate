import numpy as np
from pytz import timezone
from datetime import datetime
import pickle
import pandas as pd
import os


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


def now():
    return datetime.now(timezone('UTC')).astimezone(timezone('Asia/Tokyo')).strftime('%Y-%m-%d %H:%M:%S')


def write_file(directory, obj):
    with open(directory, mode='wb') as f:
        pickle.dump(obj, f)


def read_file(directory):
    with open(directory, mode='rb') as f:
        return pickle.load(f)


def load_data(span, folder):
    """
    取り出したデータをプロパティに持たせる
    :param span:   string ロウソク足データの時間間隔(=candle_type)  ['5min' or '15min' or '1hour']
    :param folder: string ロウソク足データがあるフォルダー名 ['data' or 'validation']
    :return: candlestick: pandas.DataFrame
    """
    if not (span is '5min' or span is '15min' or span is '1hour'):
        raise FileNotFoundError("'5min' or '15min' or '1hour'")
    cur = os.path.dirname(os.path.abspath(__file__))
    files_path = os.path.abspath(cur + '/../') + '/' + span + '/' + folder

    # 文字列なので順番はバラバラ
    files = os.listdir(files_path)

    # ファイル名前半の20180101のようなものをintに変換してソート
    files = sorted(files, key=lambda x: int(x.split('.')[0]))
    candlestick = []
    for i in range(len(files)):
        file = files_path + '/' + files[i]
        with open(file, 'rb') as f:
            result = pickle.load(f)
        candlestick.append(result)
    candlestick = pd.concat(candlestick, ignore_index=True)
    return candlestick[['open', 'end', 'low', 'high']].astype(float)


def over_write_file(directory, line_):
    """
    ファイルを上書き(一行追加)
    :param directory: string
    :param l: string
    """
    with open(directory, 'a') as f:
        f.write(l)
