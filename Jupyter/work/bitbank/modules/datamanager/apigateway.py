import python_bitbankcc


class ApiGateway:
    """
    BitBankのAPIをたたいて情報を取り出すクラス
    """

    def __init__(self, pair):
        """
        :param pair:       string コインの種類
        """
        self._pair = pair
        self._pub = python_bitbankcc.public()

    def use_ticker(self):
        """
        BitBankのティッカーapiをたたく
        :return: dict ティッカー
        """
        return self._pub.get_ticker(self._pair)

    def use_depth(self):
        """
        BitBankの板情報apiをたたく
        :return: dict 板情報
        """
        return self._pub.get_depth(self._pair)

    def use_candlestick(self, time, candle_type):
        """
        BitBankのロウソク足apiをたたく
        timeとcandle_typeの組み合わせによってはBitBankのAPIはnullを返すことがある。
        日付を指定するときは'8hour'よりも短い間隔である必要がある
        :param time:        string ex) 20180901
        :param candle_type: string
        :return:
        """
        return self._pub.get_candlestick(self._pair, candle_type, time)
