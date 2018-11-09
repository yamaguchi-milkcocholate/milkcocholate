from modules.scheduler.scheduler import Scheduler


class RealTimeTest:
    """
    1. Schedulerインスタンスを持つ
    2. processingメソッドが実行する処理である
    3. Schedulerインスタンス callメソッドでRealTimeTestインスタンスを渡す
    """

    def __init__(self, trader):
        self.__scheduler = None
        self.__trader = trader
        self.__bitcoin_position = None
        self.__yen_position = None

    def __call__(self, start, end, second):
        self.__scheduler = Scheduler(
            runner=self,
            start=start,
            end=end,
            second=second
        )

    def processing(self):
        """
        現在の板情報を取り出し行動を決める
        :return:
        """
        pass

    def __fetch_info(self):
        pass
