import os
import sys
sys.path.append(os.pardir)
from bitbank.bot import Bot
from bitbank.adviser.bollingerband_ti import BollingerBandTiAdviser

api_key = ''
api_secret = ''
adviser = BollingerBandTiAdviser(
    stock_term=20,
    inclination_alpha=400,
    pair='xrp_jpy'
)
bot = Bot(
    host='localhost',
    population_id=271,
    genome_id=0,
    adviser=adviser,
    pair='xrp_jpy',
    api_key=api_key,
    api_secret=api_secret
)

bot()
