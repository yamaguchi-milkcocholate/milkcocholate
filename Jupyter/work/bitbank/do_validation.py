from modules.backtest.validation import Validation
from modules.trader.bollingerband_validation import BollingerBandValidationTrader


trader = BollingerBandValidationTrader(
    stock_term=20,
    inclination_alpha=400
)
trader.set_genome(
    host='localhost',
    population_id=145,
    individual_num=15
)

validation = Validation(
    trader=trader
)

validation(
    candle_type='5min',
    should_log=False,
    host=None
)
