from bitbank.prototype import Prototype
from bitbank.adviser.zigzag import ZigZagAdviser
from bitbank.scheduler import Scheduler


adviser = ZigZagAdviser(init_max_high=33.5, init_min_low=33.0)

bot = Prototype(
    adviser=adviser,
    pair='xrp_jpy',
)

scheduler = Scheduler(runner=bot)
scheduler()
