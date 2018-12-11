import pickle
import os
import pandas as pd


class Picker:
    """
    pickleファイルのデータを取り出す
    """

    def __init__(self, span, use_of_data, coin, is_inclination=False):
        if use_of_data == 'training' and coin == 'btc':
            self._candlestick = self.load_data(span, folder='data', is_inclination=is_inclination)
        elif use_of_data == 'validation' and coin == 'btc':
            self._candlestick = self.load_data(span, folder='validation', is_inclination=is_inclination)
        elif use_of_data == 'training' and coin == 'xrp':
            self._candlestick = self.load_data(span, folder='data_xrp', is_inclination=is_inclination)
        elif use_of_data == 'validation' and coin == 'xrp':
            self._candlestick = self.load_data(span, folder='validation_xrp', is_inclination=is_inclination)
        else:
            raise TypeError('invalid use of data')

    @staticmethod
    def load_data(span, folder, is_inclination):
        """
        取り出したデータをプロパティに持たせる
        :param span:   string ロウソク足データの時間間隔(=candle_type)  ['5min' or '15min' or '1hour']
        :param folder: string ロウソク足データがあるフォルダー名 ['data' or 'validation']
        :param is_inclination bool
        :return: candlestick: pandas.DataFrame
        """
        if not (span is '5min' or span is '15min' or span is '1hour'):
            raise FileNotFoundError("'5min' or '15min' or '1hour'")
        cur = os.path.dirname(os.path.abspath(__file__))
        files_path = os.path.abspath(cur + '/../../') + '/' + span + '/' + folder

        # 文字列なので順番はバラバラ
        files = os.listdir(files_path)

        # ファイル名前半の20180101のようなものをintに変換してソート
        files = sorted(files, key=lambda x: int(x.split('.')[0]))
        if is_inclination:
            files = files[len(files) - 15:]
        candlestick = []
        for i in range(len(files)):
            file = files_path + '/' + files[i]
            with open(file, 'rb') as f:
                result = pickle.load(f)
            candlestick.append(result)
        candlestick = pd.concat(candlestick, ignore_index=True)
        return candlestick

    def get_candlestick(self):
        return self._candlestick
