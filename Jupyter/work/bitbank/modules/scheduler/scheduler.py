import sched
import datetime
import time


class Scheduler:

    def __init__(self, runner, start, end, second):
        """
        :param runner: object
        :param start: tuple
        :param end: tuple
        :param second:
        """
        self.runner = runner
        self.start = datetime.datetime(start[0], start[1], start[2], start[3], start[4], start[5])
        self.end = datetime.datetime(end[0], end[1], end[2], end[3], end[4], end[5])
        self.second = datetime.datetime(second[0], second[1], second[2], second[3], second[4], second[5])
        self.scheduler = sched.scheduler(time.time, time.sleep)

    def __call__(self):
        """
        スケジューラ実行
        :return: Runnerクラス(定期実行で実際に実行するprocessingメソッドをもつクラスのインスタンス)
        """
        self.schedule()
        print('end of schedule')
        return self.runner

    def processing(self, *args):
        """
        定期実行で実際に実行する処理
        :param args:
        :return:
        """
        self.runner.processing()

    def schedule(self):
        """
        スケジュールを設定
        :return:
        """
        print('start ', self.start)
        print('second', self.second)
        print('end   ', self.end)
        print()

        time_i = int(time.mktime(self.start.timetuple()))
        span = int(time.mktime(self.second.timetuple()) - time_i)
        while time_i <= int(time.mktime(self.end.timetuple())):
            self.scheduler.enterabs(time_i, 1, self.processing, argument=(datetime.datetime.fromtimestamp(time_i),))
            time_i += span
        self.scheduler.run()
