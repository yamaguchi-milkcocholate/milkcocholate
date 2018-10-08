import pickle
import urllib.request
import json
import pprint
import pandas as pd
from modules.datamanager import apigateway
import datetime
import os
import sys


class GetVariable:
    """
    指定した日付のろうそく足データを取得する
    """

    def __init__(self):
        self.test_list = list()

    def get_variable(self, timespace, start_day, finish_day,url_header,pair):
        save_dir = './data/'
        dayformat = '%Y%m%d'
        day = datetime.datetime.strptime(start_day, dayformat)
        end_day = datetime.datetime.strptime(finish_day, dayformat)
        iteration = 0
        gateway = apigateway.ApiGateway(url_header, pair)
        while iteration < 5000:
            day_str = day.strftime(dayformat)
            print(day_str)
            print(timespace)
            print(type(day_str))
            print(type(timespace))
            my_dict = gateway.use_candlestick(day_str, timespace)
            candlestick = my_dict['candlestick'][0]['ohlcv']

            df = pd.DataFrame(candlestick, columns=['open', 'high', 'low', 'end', 'turnover', 'time'])
            # timeformat
            df['time'] = pd.to_datetime(df['time'], unit='ms')
            # save

            cur = os.path.dirname(os.path.abspath(__file__))
            our = os.path.abspath(cur+'/../../')
            wur = our+'/'+timespace
            save_file = wur+save_dir + day_str + '_' + timespace + '.pkl'
            with open(save_file, 'wb') as f:
                print('saving' + day_str)
                pickle.dump(df, f)
                self.test_list.append(df)
            day += datetime.timedelta(days=1)
            if day >= end_day:
                print("成功")
                break
            iteration +=1
        if iteration > 4999:
            print("保存したい日にちが5000日を超えたため5000日でストップしました")

    def get_test_list(self):
        return self.test_list