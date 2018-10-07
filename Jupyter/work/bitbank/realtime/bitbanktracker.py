import os
import sys
sys.path.append(os.pardir)
from modules.datamanager import realtimerunner
from modules.scheduler import scheduler


class BitBankTracker:
    """
    BitBankのティッカーと板情報を定期実行で表示する
    """
    def __init__(self, url_header, pair):
        """
        :param url_header: string
        :param pair:       string
        """
        self.runner = realtimerunner.RealTimeRunner(url_header, pair)

    def __call__(self, start, end, second):
        sche = scheduler.Scheduler(self.runner, start, end, second)
        self.runner = sche()
        print('*******************************************************************')
        self.runner.show_ticker_list()
        self.runner.show_depth_list()
