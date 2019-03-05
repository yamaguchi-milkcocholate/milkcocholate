from bitbank.gp.gp import GeneticNetwork
from bitbank.gp.aggregate import Aggregate
from bitbank.gp.fitnessfunction.tag_next import TagNextFitnessFunction
import sys
from bitbank.functions import write_file, read_file
sys.setrecursionlimit(100000)

gp = read_file(directory='15min/training/aggregate_gp_04.pkl')
buy_genome = gp.get_elite_genome()

fitness_function = TagNextFitnessFunction(ema_term=6, ma_term=6, goal=0.1, buy_genome=buy_genome, limit=50)

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
gp.generation(steps=200)
# gp = read_file(directory='15min/training/gp_06.pkl')
# gp.additional_generation(steps=200)


write_file(directory='15min/training/gp_next_06.pkl', obj=gp)
