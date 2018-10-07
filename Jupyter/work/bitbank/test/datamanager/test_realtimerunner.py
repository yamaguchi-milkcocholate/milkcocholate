# coding:utf-8
import unittest
import sys
import os
import datetime
sys.path.append(os.pardir+'/../')
from modules.scheduler import scheduler
from modules.datamanager import realtimerunner


class TestRealTimeRunner(unittest.TestCase):
    """
    スケジューラでRunnerクラスが実行できるかのチェック
    """

    def setUp(self):
        self.runner = realtimerunner.RealTimeRunner('http://192.168.99.100:10080', 'btc_jpy')

    def test_schedule(self):
        now = datetime.datetime.now()
        start = (now.year, now.month, now.day, now.hour, now.minute, now.second)
        end = (now.year, now.month, now.day, now.hour, now.minute, now.second + 6)
        second = (now.year, now.month, now.day, now.hour, now.minute, now.second + 2)
        sche = scheduler.Scheduler(self.runner, start, end, second)
        self.runner = sche()
        self.assertEqual(len(self.runner.ticker_list), 4)
        self.assertEqual(len(self.runner.depth_list), 4)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
