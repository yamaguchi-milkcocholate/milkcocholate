from modules.backtest.validation import Validation
from modules.trader.bollingerband_sma_ti_validation import BollingerBandSMATiValidationTrader


trader = BollingerBandSMATiValidationTrader(
    stock_term=20,
    inclination_alpha=9
)
trader.set_genome(
    host='localhost',
    population_id=384,
    individual_num=0
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
