from modules.feature import functions
from modules.backtest import backtest


situation = functions.bollinger_band()

candle_type = '1hour'
population = 3
mutation = 50
cross = 2
elite_num = 1
host = 'localhost'
fitness_function_name = 'bollinger_band_linear_end'
crossover_name = 'uniform'
hyper_params = dict()
hyper_params['sma_term'] = 10
hyper_params['std_term'] = 5
hyper_params['last_data_num'] = 5
hyper_params['inclination_alpha'] = 1000

back_test = backtest.BackTest(situation=situation,
                              candle_type=candle_type,
                              population=population,
                              mutation=mutation,
                              cross=cross,
                              elite_num=elite_num,
                              host=host,
                              fitness_function_name=fitness_function_name,
                              crossover_name=crossover_name,
                              hyper_params=hyper_params
                              )

back_test(steps=6, log_span=2)
