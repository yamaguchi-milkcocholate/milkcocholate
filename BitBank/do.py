from bitbank.bot import Bot
from bitbank.adviser.bollingerband_ti import BollingerBandTiAdviser
from bitbank.scheduler import Scheduler


print('api_key: ', end='')
api_key = input()

print('api_secret: ', end='')
api_secret = input()

print('host: ', end='')
host = input()

print('population id: ', end='')
population_id = input()
population_id = int(population_id)

print('genome id: ', end='')
genome_id = input()
genome_id = int(genome_id)

adviser = BollingerBandTiAdviser(
    stock_term=12,
    inclination_alpha=2,
    pair='xrp_jpy'
)

bot = Bot(
    host=host,
    population_id=population_id,
    genome_id=genome_id,
    adviser=adviser,
    pair='xrp_jpy',
    api_key=api_key,
    api_secret=api_secret
)

scheduler = Scheduler(runner=bot)
scheduler()
