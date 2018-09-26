import pickle
import os
import pandas as pd


class Picker:

    def __init__(self, span):
        self.candlestick = self.load_data(span)

    @staticmethod
    def load_data(span):
        if not (span is '5min' or span is '15min' or span is '1hour'):
            raise FileNotFoundError("'5min' or '15min' or '1hour'")
        files_path = os.path.abspath(__file__) + '/../../../' + span + '/data'
        files = os.listdir(files_path)

        candlestick = []
        for i in range(len(files)):
            file = files_path + '/' + files[i]
            with open(file, 'rb') as f:
                result = pickle.load(f)
            candlestick.append(result)
        candlestick = pd.concat(candlestick, ignore_index=True)
        return candlestick

    def get_candlestick(self):
        return self.candlestick
