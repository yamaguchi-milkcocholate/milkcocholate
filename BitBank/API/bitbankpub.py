import python_bitbankcc


class BitBankPubAPIManager:

    def __init__(self):
        """
        constructor
        """
        self.pub = python_bitbankcc.public()

    def get_ticker(self, pair):
        """
        getting market price
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
        getting board information
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
        getting contract history
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
        getting candlestick information
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
