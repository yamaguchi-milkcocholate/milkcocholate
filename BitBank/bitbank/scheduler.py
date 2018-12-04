import sched
import datetime
import time
import sys
from pytz import timezone
from bitbank.exceptions.schedcancel import SchedulerCancelException


class Scheduler:

    def __init__(self, runner):
        self.__runner = runner
        self.__scheduler = sched.scheduler(time.time, time.sleep)

    def __call__(self):
        self.__schedule()

    def __schedule(self):
        now = datetime.datetime.now(timezone('UTC')).astimezone(timezone('Asia/Tokyo'))
        now_5min = now + datetime.timedelta(minutes=5)
        now_a_week = now + datetime.timedelta(days=7)
        print('Start at ' + now.strftime('%Y-%m-%d %H:%M:%S'))

        time_i = int(time.mktime(now.timetuple()))
        span = int(time.mktime(now_5min.timetuple()) - time_i)
        a_week = int(time.mktime(now_a_week.timetuple()))
        while time_i <= a_week:
            self.__scheduler.enterabs(
                time_i,
                1,
                self.__processing,
                argument=(datetime.datetime.fromtimestamp(time_i).strftime('%Y-%m-%d %H:%M:%S'),)
            )
            time_i += span
        self.__scheduler.run()
        print('Finish at ' + datetime.datetime.fromtimestamp(time_i - span).strftime('%Y-%m-%d %H:%M:%S'))

    def __processing(self, *args):
        try:
            print('Execute at ' + args[0])
            self.__runner()
        except SchedulerCancelException as e:
            # スケジューラをキャンセル
            print(e.get_message())
            sys.exit()
