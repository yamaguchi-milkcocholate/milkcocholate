import urllib.request
import json


class ApiGateway:
    """
    BitBankのAPIをたたいて情報を取り出すクラス
    """

    def __init__(self, url_header, pair):
        """
        :param url_header: string urlの先頭(クラウド or ローカル)
        :param pair:       string コインの種類
        """
        self._url_header = url_header
        self._pair = pair

    def use_ticker(self):
        """
        BitBankのティッカーapiをたたく
        :return: dict ティッカー
        """
        ticker_url = self._url_header + '/public/ticker/' + self._pair
        req_ticker = urllib.request.Request(ticker_url)
        with urllib.request.urlopen(req_ticker) as res:
            body = res.read()
        return json.loads(body.decode('utf-8'))

    def use_depth(self):
        """
        BitBankの板情報apiをたたく
        :return: dict 板情報
        """
        depth_url = self._url_header + '/public/depth/' + self._pair
        req_depth = urllib.request.Request(depth_url)
        with urllib.request.urlopen(req_depth) as res:
            body = res.read()
        return json.loads(body.decode('utf-8'))

    def use_candlestick(self, time, candle_type):
        """
        BitBankのロウソク足apiをたたく
        timeとcandle_typeの組み合わせによってはBitBankのAPIはnullを返すことがある。
        日付を指定するときは'8hour'よりも短い間隔である必要がある
        :param time:        string ex) 20180901
        :param candle_type: string
        :return:
        """
        url = self._url_header + '/public/candlestick/' + self._pair + '/'+candle_type+'?time=' + time
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as res:
            body = res.read()
        return json.loads(body.decode('utf-8'))
