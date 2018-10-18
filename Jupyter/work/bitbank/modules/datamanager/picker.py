import pickle
import os
import pandas as pd
import pprint


class Picker:
    """
    pickleファイルのデータを取り出す
    """

    def __init__(self, span):
        self._candlestick = self.load_data(span)

    @staticmethod
    def load_data(span):
        """
        取り出したデータをプロパティに持たせる
        :param span: string ロウソク足データの時間間隔(=candle_type)  ['5min' or '15min' or '1hour']
        :return:
        """
        if not (span is '5min' or span is '15min' or span is '1hour'):
            raise FileNotFoundError("'5min' or '15min' or '1hour'")
        cur = os.path.dirname(os.path.abspath(__file__))
        files_path = os.path.abspath(cur + '/../../') + '/' + span + '/data'

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
        return candlestick

    def get_candlestick(self):
        return self._candlestick
