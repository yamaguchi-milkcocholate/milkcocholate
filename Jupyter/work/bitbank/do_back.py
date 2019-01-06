from modules.feature import functions
from modules.backtest import backtest


situation = functions.macd()

candle_type = '5min'
population = 3
mutation = 2
cross = 50
elite_num = 1
host = 'localhost'
fitness_function_name = 'zigzag'
crossover_name = 'uniform'
hyper_params = dict()

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

back_test(steps=1, log_span=20)
