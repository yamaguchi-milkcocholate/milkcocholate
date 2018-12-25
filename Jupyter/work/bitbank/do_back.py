from modules.feature import functions
from modules.backtest import backtest


situation = functions.macd()

candle_type = '5min'
population = 30
mutation = 2
cross = 50
elite_num = 2
host = '192.168.99.100'
fitness_function_name = 'macd'
crossover_name = 'uniform'
hyper_params = dict()
hyper_params['short_term'] = 12
hyper_params['long_term'] = 26
hyper_params['signal'] = 9

back_test = backtest.BackTest(situation=situation,
                              candle_type=candle_type,
                              pair='xrp',
                              population=population,
                              mutation=mutation,
                              cross=cross,
                              elite_num=elite_num,
                              host=host,
                              fitness_function_name=fitness_function_name,
                              crossover_name=crossover_name,
                              hyper_params=hyper_params
                              )

back_test(steps=1, log_span=10)
