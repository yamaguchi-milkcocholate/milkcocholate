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
    buy_directory='15min/training/buy_20190312.pkl',
    sell_directory='15min/training/sell_20190312.pkl'
)

bot = Bot(
    adviser=adviser,
    pair='xrp_jpy',
    api_key=api_key,
    api_secret=api_secret,
    log='log/20190311.txt',
    limit=50
)

scheduler = Scheduler(runner=bot)
scheduler()
