import datetime
from modules.realtimetest.realtimetest import RealTimeTest
from modules.trader.bollingerband import BollingerBandTrader


trader = BollingerBandTrader(
    stock_term=26,
    inclination_alpha=2000,
    candle_type='5min'
)
trader.set_genome(host='localhost', population_id=97)

# 3秒スパンで3回
now = datetime.datetime.now()
start = (now.year, now.month, now.day, now.hour, now.minute, now.second + 1)
end = (now.year, now.month, now.day, now.hour, now.minute + 1, now.second)
second = (now.year, now.month, now.day, now.hour, now.minute, now.second + 6)

test = RealTimeTest(trader=trader)
test(
    start=start,
    end=end,
    second=second,
    should_log=True,
    host='localhost'
)
