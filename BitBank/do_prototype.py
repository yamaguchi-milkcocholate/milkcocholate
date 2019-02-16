from bitbank.prototype import Prototype
from bitbank.adviser.tag import Tag
from bitbank.scheduler import Scheduler


adviser = Tag(ema_term=3, ma_term=6, directory='15min/training/gp_04.pkl')

bot = Prototype(
    adviser=adviser,
    pair='xrp_jpy',
    log='genome_04.txt'
)

scheduler = Scheduler(runner=bot)
scheduler()
