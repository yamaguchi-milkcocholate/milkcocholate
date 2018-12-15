from modules.backtest.validation import Validation
from modules.trader.bollingerband_ti_validation import BollingerBandValidationTrader


trader = BollingerBandValidationTrader(
    stock_term=20,
    inclination_alpha=9
)
trader.set_genome(
    host='192.168.99.100',
    population_id=365,
    individual_num=9
)

validation = Validation(
    trader=trader
)

validation(
    candle_type='5min',
    coin='xrp',
    should_log=False,
    host=None
)
