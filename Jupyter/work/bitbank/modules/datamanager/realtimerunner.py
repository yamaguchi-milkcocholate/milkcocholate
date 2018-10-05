# coding:utf-8
import urllib.request
import json
import pprint


class RealTimeRunner:

    def __init__(self, pair):
        self.ticker_url = 'http://192.168.99.100:10080/public/ticker/' + pair
        self.depth_url = 'http://192.168.99.100:10080/public/depth/' + pair
        self.ticker_list = list()
        self.depth_list = list()

    def processing(self, *args):
        """
        スケジューラで実行する処理
        現在の板情報とティッカーのAPIをたたく
        :param args:
        :return:
        """
        req_ticker = urllib.request.Request(self.ticker_url)
        req_depth = urllib.request.Request(self.depth_url)
        with urllib.request.urlopen(req_ticker) as res:
            body = res.read()
        self.ticker_list.append(json.loads(body.decode('utf-8')))

        with urllib.request.urlopen(req_depth) as res:
            body = res.read()
        self.depth_list.append(json.loads(body.decode('utf-8')))

        pprint.pprint(self.ticker_list[len(self.ticker_list) - 1])
        pprint.pprint(self.depth_list[len(self.depth_list) - 1])

    def show_ticker_list(self):
        pprint.pprint(self.ticker_list)

    def show_depth_list(self):
        pprint.pprint(self.depth_list)
