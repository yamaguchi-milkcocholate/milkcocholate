import python_bitbankcc


class BitBankPubAPIManager:

    def __init__(self):
        """
        コンストラクタ
        """
        self.pub = python_bitbankcc.public()

    def get_ticker(self, pair):
        """
        市場価格を取得
        :param pair:
        :return:
        """
        try:
            value = self.pub.get_ticker(pair)
            return value
        except Exception as e:
            print(e)
            return None

    def get_depth(self, pair):
        """
        板情報を取得
        :param pair:
        :return:
        """
        try:
            value = self.pub.get_depth(pair)
            return value
        except Exception as e:
            print(e)
            return None

    def get_transactions(self, pair, time=None):
        """
        約定履歴を取得
        :param pair:
        :param time:
        :return:
        """
        try:
            value = self.pub.get_transactions(pair, time)
            return value
        except Exception as e:
            print(e)
            return None

    def get_candlestick(self, pair, candle_type, time=None):
        """
        ロウソク足データを取得
        :param pair:
        :param candle_type:
        :param time:
        :return:
        """
        try:
            value = self.pub.get_candlestick(pair, candle_type, time)
            return value
        except Exception as e:
            print(e)
            return None
