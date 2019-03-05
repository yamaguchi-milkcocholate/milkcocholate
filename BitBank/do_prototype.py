from bitbank.prototype import Prototype
from bitbank.adviser.tag import Tag
from bitbank.scheduler import Scheduler


adviser = Tag(ema_term=3, ma_term=6, buy_directory='15min/training/aggregate_gp_03.pkl', sell_directory='15min/training/gp_next_04.pkl')

bot = Prototype(
    adviser=adviser,
    pair='xrp_jpy',
    log='15min/log/genome_01.txt'
)

scheduler = Scheduler(runner=bot)
scheduler()
