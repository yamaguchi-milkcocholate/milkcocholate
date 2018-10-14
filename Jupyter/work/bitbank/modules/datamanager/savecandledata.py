import pickle
import urllib.request
import json
import pprint
import pandas as pd
from modules.datamanager import apigateway
import os
import sys
import datetime


class SaveCandleData:
    """
    指定した日付のろうそく足データを取得する
    """

    def __init__(self):
        self.test_list = list()

    def save_candledata(self, timespace, start_day, finish_day, url_header, pair):
        """
           指定した日付のろうそく足データを取得する
           引数には（時間間隔,調べたい期間の最初の日,調べたい期間の最後の日,urlヘッダー,仮想通貨の名前）
           """

        save_dir = './data/'
        dayformat = '%Y%m%d'
        day = datetime.datetime.strptime(start_day, dayformat)
        end_day = datetime.datetime.strptime(finish_day, dayformat)
        datetime.datetime.today().strftime("%Y%m%d")
        if int(datetime.datetime.today().strftime("%Y%m%d")) < int(finish_day):
            print("調べたい期間が未来を含んでいます")
            sys.exit()
        if int(start_day)>int(finish_day):
            print("調べたい期間の最初の日付が最後の日付より後になっています")
            sys.exit()
        gateway = apigateway.ApiGateway(url_header, pair)
        cur = os.path.dirname(os.path.abspath(__file__))
        our = os.path.abspath(cur + '/../..')
        wur = our + '/' + timespace
        while day <= end_day:
            day_str = day.strftime(dayformat)
            my_dict = gateway.use_candlestick(day_str, timespace)
            candlestick = my_dict['candlestick'][0]['ohlcv']

            df = pd.DataFrame(candlestick, columns=['open', 'high', 'low', 'end', 'turnover', 'time'])
            # timeformat
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            # save
            save_file = wur + save_dir + day_str + '_' + timespace + '.pkl'
            with open(save_file, 'wb') as f:
                print('saving' + day_str)
                pickle.dump(df, f)
                self.test_list.append(df)
            day += datetime.timedelta(days=1)
        print("終了しました")

    def get_test_list(self):
        return self.test_list