# coding:utf-8
import unittest
import sys
import os
import datetime
sys.path.append(os.pardir+'/../')
from modules.scheduler import scheduler


class TestScheduler(unittest.TestCase):

    def setUp(self):
        pass

    def test_schedule(self):
        """
        現在時刻を含めて3秒後まで1秒間隔で実行
        :return:
        """
        self.runner = SampleRunner()
        now = datetime.datetime.now()
        start = (now.year, now.month, now.day, now.hour, now.minute, now.second)
        end = (now.year, now.month, now.day, now.hour, now.minute, now.second + 3)
        second = (now.year, now.month, now.day, now.hour, now.minute, now.second + 1)
        sche = scheduler.Scheduler(self.runner, start, end, second)
        self.runner = sche()
        print(self.runner.tracker)
        self.assertEqual(self.runner.tracker[0].strftime('%Y-%m-%d %H:%M:%S'),
                         str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2) + ' '
                         + str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(now.second).zfill(2))
        self.assertEqual(self.runner.tracker[1].strftime('%Y-%m-%d %H:%M:%S'),
                         str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2) + ' '
                         + str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(now.second + 1).zfill(2))
        self.assertEqual(self.runner.tracker[2].strftime('%Y-%m-%d %H:%M:%S'),
                         str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2) + ' '
                         + str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(now.second + 2).zfill(2))
        self.assertEqual(self.runner.tracker[3].strftime('%Y-%m-%d %H:%M:%S'),
                         str(now.year) + '-' + str(now.month).zfill(2) + '-' + str(now.day).zfill(2) + ' '
                         + str(now.hour).zfill(2) + ':' + str(now.minute).zfill(2) + ':' + str(now.second + 3).zfill(2))

    def tearDown(self):
        pass


class SampleRunner:

    def __init__(self):
        self.tracker = list()

    def processing(self, time_at=None):
        self.tracker.append(time_at)


if __name__ == '__main__':
    unittest.main()
