from bitbank.apigateway import ApiGateway
from bitbank.line import Line
from bitbank.functions import *
from bitbank.exceptions.schedcancel import SchedulerCancelException


class Auto:
    BUY = 1
    STAY = 2
    SELL = 3
    RETRY = 4

    DEFAULT_TYPE = 'market'
    TYPE_LIMIT = 'limit'
    TYPE_MARKET = 'market'

    def __init__(self, adviser, pair, api_key=None, api_secret=None):
        """
        :param adviser:       bitbank.adviser テクニカル分析結果から売却の指示をするクラスのインスタンス
        :param pair:          string          通貨のペア
        :param api_key:
        :param api_secret:
        """
        self.adviser = adviser
        self.pair = pair
        self.coin = pair.split('_')[0]
        self.yen = pair.split('_')[1]
        self.api_gateway = ApiGateway(api_key=api_key, api_secret=api_secret)
        self.buying_price = None
        self.order_ids = None
        self.__line = Line()
        self.__start_price = self.fetch_price()

    def fetch_price(self):
        """
        開始時の価格を返す
        :return: string
        """
        ticker = self.api_gateway.use_ticker(pair=self.pair)
        return float(ticker['last'])

    @staticmethod
    def __side_to_japanese(side):
        if side == 'buy':
            japanese = '買い'
        else:
            japanese = '売り'
        return japanese

    @staticmethod
    def __status_to_japanese(status):
        if status == 'UNFILLED':
            japanese = '注文中'
        elif status == 'PARTIALLY_FILLED':
            japanese = '注文中(一部約定)'
        elif status == 'FULLY_FILLED':
            japanese = '約定済み'
        elif status == 'CANCELED_UNFILLED':
            japanese = '取消済'
        elif status == 'CANCELED_PARTIALLY_FILLED':
            japanese = '取消済(一部約定)'
        else:
            japanese = None
        return japanese

    def loss_cut_message(self):
        message = "損切りを行いました。"
        self.__line(message=message)

    def error_message(self, message):
        message = "エラー発生!!\n" \
                  "===================\n" \
                  "" + message + "\n" \
                  "==================="
        self.__line(message=message)

    def market_selling_message(self):
        message = "指値売り注文をキャンセルしましたので、成行注文を行います。"
        self.__line(message=message)

    def cancel_order_message(self, result):
        side = self.__side_to_japanese(side=result['side'])
        status = self.__status_to_japanese(status=result['status'])
        message = "注文を取り消しました。\n" \
                  "===================\n" \
                  "" + result['pair'] + " " + side + "注文 " + status + "\n" \
                  "注文ID: {}\n" \
                  "時刻: {}\n" \
                  "価格: {}\n" \
                  "平均価格: {}\n" \
                  "数量: {}\n" \
                  "約定数量: {}\n" \
                  "===================".format(
                        result['order_id'],
                        now(),
                        result['price'],
                        result['average_price'],
                        result['start_amount'],
                        result['executed_amount'],
                  )
        message.replace('n', '%0D%0A')
        self.__line(message=message)

    def new_order_message(self, order, retry):
        side = self.__side_to_japanese(side=order.side)
        status = self.__status_to_japanese(status=order.status)
        message = "新規注文を行いました。\n" \
                  "===================\n" \
                  "" + order.pair + " " + side + "注文 " + status + "\n" \
                  "注文ID: {}\n" \
                  "時刻: {}\n" \
                  "価格: {}\n" \
                  "数量: {}\n" \
                  "再要求回数: {}\n" \
                  "===================".format(
                        order.order_id,
                        order.ordered_at,
                        order.price,
                        order.start_amount,
                        retry
                  )
        message.replace('n', '%0D%0A')
        self.__line(message=message)

    def __operation_to_side(self, operation):
        if operation == int(self.BUY):
            return 'buy'
        elif operation == int(self.SELL):
            return 'sell'
        else:
            raise SchedulerCancelException()
