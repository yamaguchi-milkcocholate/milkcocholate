from bitbank.gp.gp import GeneticNetwork
from bitbank.gp.aggregate import Aggregate
from bitbank.gp.fitnessfunction.tag import TagFitnessFunction
import sys
from bitbank.functions import write_file, read_file
sys.setrecursionlimit(100000)

fitness_function = TagFitnessFunction(ema_term=4, ma_term=8, goal=0.2, data='15min')
aggregate = Aggregate(
    gp_num=3,
    mutation=5,
    cross=50,
    elite_num=3,
    population=50,
    new_num=3,
    fitness_function=fitness_function,
    keep=40,
    depth=15,
    steps=200
)

"""
gp = GeneticNetwork(
    mutation=5,
    cross=50,
    elite_num=2,
    population=100,
    new_num=10,
    fitness_function=fitness_function,
    keep=10,
    depth=15
)
gp.init_population()
gp.generation(steps=300)
#gp = read_file(directory='15min/training/gp_06.pkl')
#gp.additional_generation(steps=200)
"""

write_file(directory='15min/training/aggregate_gp_09.pkl', obj=aggregate)
