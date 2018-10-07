import os
import sys
import datetime
sys.path.append(os.pardir)
from modules.datamanager import realtimerunner
from modules.scheduler import scheduler



runner = realtimerunner.RealTimeRunner('btc_jpy')
now = datetime.datetime.now()
start = (now.year, now.month, now.day, now.hour, 30, 0)
end = (now.year, now.month, now.day, now.hour + 1, 30, 0)
second = (now.year, now.month, now.day, now.hour, 35, 0)
sche = scheduler.Scheduler(runner, start, end, second)
runner = sche()
print('*******************************************************************')
runner.show_ticker_list()
runner.show_depth_list()
