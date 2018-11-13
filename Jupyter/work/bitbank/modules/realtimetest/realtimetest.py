from modules.scheduler.scheduler import Scheduler
from modules.datamanager.apigateway import ApiGateway
import datetime


class RealTimeTest:
    BUY = 1
    SELL = 2
    STAY = 3
    DEFALT_BITCOIN_AMOUNT = 1
    """
    1. Schedulerインスタンスを持つ
    2. processingメソッドが実行する処理である
    3. Schedulerインスタンス callメソッドでRealTimeTestインスタンスを渡す
    """

    def __init__(self, trader):
        self.__scheduler = None
        self.__trader = trader
        self.__bitcoin_position = self.DEFALT_BITCOIN_AMOUNT
        self.__yen_position = 0
        self.__has_bitcoin = True
        self.__api_gateway = ApiGateway('btc_jpy')

    def __call__(self, start, end, second, should_log):
        self.__scheduler = Scheduler(
            runner=self,
            start=start,
            end=end,
            second=second
        )
        self.__should_log = should_log
        self.__scheduler()

    def processing(self):
        """
        定期実行する内容
        データを更新、計算、行動を決定させる
        取引結果を表示、記録
        """
        operation = self.__trader.operation()
        if operation is self.BUY and self.__has_bitcoin is False:
            last_price, time = self.__fetch_ticker()
            self.__bitcoin_position = float(self.__yen_position / last_price)
            self.__yen_position = 0
            self.__has_bitcoin = True
            print(
                time,
                'last price', ': {:<10}'.format(last_price),
                'yen position', ': {:<10}'.format(self.__yen_position),
                'bitcoin position', ': {:<10}'.format(self.__bitcoin_position),
            )
        elif operation is self.SELL and self.__has_bitcoin is True:
            last_price, time = self.__fetch_ticker()
            self.__yen_position = float(self.__bitcoin_position * last_price)
            self.__bitcoin_position = 0
            self.__has_bitcoin = False
            print(
                time,
                'last price', ': {:<10}'.format(last_price),
                'yen position', ': {:<10}'.format(self.__yen_position),
                'bitcoin position', ': {:<10}'.format(self.__bitcoin_position),
            )
        elif operation is self.STAY:
            pass

    def __fetch_ticker(self):
        """
        tickerのapiを叩いて情報を取り出す
        :return: int, datetime.datetime: 最近の取引値, データ取得時間
        """
        ticker = self.__api_gateway.use_ticker()
        # bitbankのunixtimeはミリ秒まで含めているので除外
        return int(ticker['last']), datetime.datetime.fromtimestamp(
            int(ticker['timestamp']) / 1000).strftime("%Y-%m-%d %H:%M:%S")


