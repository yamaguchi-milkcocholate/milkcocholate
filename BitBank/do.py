from bitbank.bot import Bot
from bitbank.adviser.zigzag import ZigZagAdviser
from bitbank.scheduler import Scheduler


print('api_key: ', end='')
api_key = input()

print('api_secret: ', end='')
api_secret = input()

adviser = ZigZagAdviser(init_max_high=33.5, init_min_low=33.0)

bot = Bot(
    adviser=adviser,
    pair='xrp_jpy',
    api_key=api_key,
    api_secret=api_secret
)

scheduler = Scheduler(runner=bot)
scheduler()
