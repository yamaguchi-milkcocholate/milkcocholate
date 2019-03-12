from bitbank.bot import Bot
from bitbank.adviser.tag import Tag
from bitbank.scheduler import Scheduler


print('api_key: ', end='')
api_key = input()

print('api_secret: ', end='')
api_secret = input()

adviser = Tag(
    ema_term=4,
    ma_term=8,
    buy_directory='15min/training/aggregate_gp_08.pkl',
    sell_directory='15min/training/gp_next_11.pkl'
)

bot = Bot(
    adviser=adviser,
    pair='xrp_jpy',
    api_key=api_key,
    api_secret=api_secret,
    log='log/20190311.txt'
)

scheduler = Scheduler(runner=bot)
scheduler()
