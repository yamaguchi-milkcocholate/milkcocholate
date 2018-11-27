from modules.db.facade import Facade
from modules.datamanager.picker import Picker
import matplotlib.pyplot as plt
import numpy as np


class Validation:
    BUY = 1
    SELL = 2
    STAY = 3
    DEFAULT_BITCOIN_AMOUNT = 1
    """
    学習した遺伝子について、妥当性をチェックする
    過去のデータの中で学習に使っていないものを用いて売却をシミュレーションする
    """

    def __init__(self, trader):
        self.__trader = trader
        self.__bitcoin_position = self.DEFAULT_BITCOIN_AMOUNT
        self.__yen_position = 0
        self.__has_bitcoin = True
        self.__log_dept = None
        self.__should_log = None
        self.__total = list()

    def __call__(self, candle_type, should_log=False, host=None):
        """
        取引のシミュレーションを開始する
        :param should_log: bool 記録をデータベースに保存するかどうか
        :param host:  string データベースのホスト
        """
        self.__should_log = should_log
        db_facade = None
        if self.__should_log:
            db_facade = Facade(host=host)
            self.__log_dept = db_facade.select_department('realtime_test_logs')
        # 取引シミュレーションを開始
        self.__validation(candle_type=candle_type)
        # 実験を記録
        if self.__should_log:
            real_time_test_dept = db_facade.select_department('realtime_tests')
            population_id = self.__trader.get_populaiton_id()
            real_time_test_dept.give_writer_task(values=[[population_id]])
        # plot
        plt.title('Simulation')
        # y軸
        plt.ylabel('Yen')
        # position
        total_np = np.asarray(self.__total)
        plt.ylim([0, np.max(total_np) + 100000])
        # BitBank
        batbank_np = self.__candlestick.end.tail(len(total_np)).values
        # x軸
        x_axis = np.arange(0, len(total_np))
        plt.xlabel('Index')

        plt.plot(x_axis, total_np, label='Position')
        plt.plot(x_axis, batbank_np, label='BitBank')
        plt.show()

    def __validation(self, candle_type):
        """
        取引シミュレーションを実行する関数
        :param candle_type: string ロウソク足データの期間
        """
        # 終値と取得時間のDataFrameを読み込む
        candlestick = self.__fetch_candlestick(candle_type=candle_type)
        self.__candlestick = candlestick
        # Traderにデータを渡す
        self.__trader.set_candlestick(candlestick=candlestick)
        # operation == Falseになるまでループ（ロウソク足データを使い切るまで）
        while True:
            operation = self.__trader.operation()
            if not operation:
                break
            self.__transaction_result(operation=operation)
        print('finish validation')

    @staticmethod
    def __fetch_candlestick(candle_type):
        """
        保存してあるロウソク足データ終値のpickleファイルを読み込んで返す関数
        :param candle_type: string ロウソク足データの期間
        :return: candlestick: pandas.DataFrame
        """
        candlestick = Picker(span=candle_type, use_of_data='validation').get_candlestick()
        return candlestick

    def __transaction_result(self, operation):
        """
        取引の結果を出力する。必要であればデータベースに記録する関数
        :param operation: int 取引の内容を表す値
        """
        last_price, time = self.__trader.fetch_information()
        if operation is self.BUY:
            if self.__has_bitcoin is False:
                self.__bitcoin_position = float(self.__yen_position / last_price)
                self.__yen_position = 0
                self.__has_bitcoin = True
                total = last_price * self.__bitcoin_position
                print(
                    time,
                    '       BUY',
                    'last price', ': {:<10}'.format(last_price),
                    'yen position', ': {:<10}'.format(self.__yen_position),
                    'bitcoin position', ': {:<10}'.format(self.__bitcoin_position),
                    'total', ': {:<10}'.format(total),
                )
                self.__total.append(total)
                if self.__should_log:
                    # id以外の挿入データ
                    values = [
                        int(last_price),
                        int(self.__yen_position),
                        int(self.__bitcoin_position),
                        # 資産の合計
                        int(last_price * self.__bitcoin_position),
                        time
                    ]
                    self.__log_dept.give_writer_task(values=[values])
            else:
                total = last_price * self.__bitcoin_position
                print(
                    time,
                    'CANNOT BUY',
                    'last price', ': {:<10}'.format(last_price),
                    'yen position', ': {:<10}'.format(self.__yen_position),
                    'bitcoin position', ': {:<10}'.format(self.__bitcoin_position),
                    'total', ': {:<10}'.format(total)
                )
                self.__total.append(total)
        elif operation is self.SELL:
            if self.__has_bitcoin is True:
                self.__yen_position = float(self.__bitcoin_position * last_price)
                self.__bitcoin_position = 0
                self.__has_bitcoin = False
                print(
                    time,
                    '       SELL',
                    'last price', ': {:<10}'.format(last_price),
                    'yen position', ': {:<10}'.format(self.__yen_position),
                    'bitcoin position', ': {:<10}'.format(self.__bitcoin_position),
                    'total', ': {:<10}'.format(self.__yen_position)
                )
                self.__total.append(self.__yen_position)
                if self.__should_log:
                    # id以外の挿入データ
                    values = [
                        int(last_price),
                        int(self.__yen_position),
                        int(self.__bitcoin_position),
                        # 資産の合計
                        int(self.__yen_position),
                        time
                    ]
                    self.__log_dept.give_writer_task(values=[values])
            else:
                print(
                    time,
                    'CANNOT SELL',
                    'last price', ': {:<10}'.format(last_price),
                    'yen position', ': {:<10}'.format(self.__yen_position),
                    'bitcoin position', ': {:<10}'.format(self.__bitcoin_position),
                    'total', ': {:<10}'.format(self.__yen_position)
                )
                self.__total.append(self.__yen_position)
        elif operation is self.STAY:
            if self.__yen_position > 0:
                total = self.__yen_position
            else:
                total = last_price * self.__bitcoin_position
            print(
                time,
                '       STAY',
                'last price', ': {:<10}'.format(last_price),
                'yen position', ': {:<10}'.format(self.__yen_position),
                'bitcoin position', ': {:<10}'.format(self.__bitcoin_position),
                'total', ': {:<10}'.format(total)
            )
            self.__total.append(total)
        else:
            raise TypeError('operation is invalid', operation)
