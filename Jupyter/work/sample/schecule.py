import sched, time, datetime

s = sched.scheduler(time.time, time.sleep)

et1 = datetime.datetime(2018, 5, 7, 19)  # 実行する時間の作成
et1 = int(time.mktime(et1.timetuple()))  # UNIX時間に変換

et2 = datetime.datetime(2018, 5, 7, 19, 10)
et2 = int(time.mktime(et2.timetuple()))


def processing(a):
    print(datetime.datetime.now(), a)


def schedule():
    s.enterabs(et1, 1, processing, argument=('event1',))
    s.enterabs(et2, 1, processing, argument=('event2',))
    s.run()


schedule()
