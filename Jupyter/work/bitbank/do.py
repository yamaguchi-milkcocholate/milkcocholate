from modules.feature import genofeature
from modules.backtest import backtest


situation = genofeature.Situation()
situation.set_fitness_function_id(f_id=1)
situation.set_genome_ranges(short_term=(1, 50), long_term=(51, 100), signal=(1, 50))

candle_type = '1hour'
population = 10
mutation = 50
cross = 2
elite_num = 1
host = 'localhost'
fitness_function_name = 'simple_macd_params'
crossover_name = 'uniform'

back_test = backtest.BackTest(situation=situation, candle_type=candle_type,
                              population=population, mutation=mutation, cross=cross, elite_num=elite_num, host=host,
                              fitness_function_name=fitness_function_name, crossover_name=crossover_name)

back_test(steps=30, log_span=10)
