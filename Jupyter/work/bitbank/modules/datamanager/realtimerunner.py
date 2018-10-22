# coding:utf-8
import pprint
from modules.datamanager import apigateway


class RealTimeRunner:

    def __init__(self, pair):
        self.ticker_list = list()
        self.depth_list = list()
        self.api_gateway = apigateway.ApiGateway(pair)

    def processing(self, *args):
        """
        スケジューラで実行する処理
        現在の板情報とティッカーを取り出す
        :param args:
        :return:
        """
        self.ticker_list.append(self.api_gateway.use_ticker())
        self.depth_list.append(self.api_gateway.use_depth())

    def show_ticker_list(self):
        pprint.pprint(self.ticker_list)

    def show_depth_list(self):
        pprint.pprint(self.depth_list)
