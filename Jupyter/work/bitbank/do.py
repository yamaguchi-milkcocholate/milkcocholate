from modules.feature import genofeature
from modules.backtest import backtest


situation = genofeature.Situation()
situation.set_fitness_function_id(f_id=1)
situation.set_genome_ranges(short_term=(1, 200), long_term=(201, 400), signal=(1, 100))

candle_type = '15min'
population = 15
mutation = 50
cross = 2
elite_num = 1
host = '192.168.99.100'
fitness_function_name = 'simple_macd_params'
crossover_name = 'uniform'

back_test = backtest.BackTest(situation=situation, candle_type=candle_type,
                              population=population, mutation=mutation, cross=cross, elite_num=elite_num, host=host,
                              fitness_function_name=fitness_function_name, crossover_name=crossover_name)

back_test(steps=100, log_span=20)
