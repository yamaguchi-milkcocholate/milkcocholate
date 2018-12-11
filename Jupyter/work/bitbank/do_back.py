from modules.feature import functions
from modules.backtest import backtest


situation = functions.bollinger_band_ti()

candle_type = '5min'
population = 5
mutation = 2
cross = 50
elite_num = 2
host = 'localhost'
fitness_function_name = 'bollinger_band_period_goal_ti'
crossover_name = 'uniform'
hyper_params = dict()
hyper_params['sma_term'] = 12
hyper_params['std_term'] = 12
hyper_params['last_data_num'] = 12
hyper_params['inclination_alpha'] = 2

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
