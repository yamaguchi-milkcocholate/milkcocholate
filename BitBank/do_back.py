from bitbank.gp.gp import GeneticNetwork
from bitbank.gp.fitnessfunction.tag import TagFitnessFunction
import sys
from bitbank.functions import write_file, read_file
sys.setrecursionlimit(100000)

fitness_function = TagFitnessFunction(ema_term=3, ma_term=6, goal=0.2)

gp = GeneticNetwork(mutation=5, cross=50, elite_num=2, population=100, new_num=10, fitness_function=fitness_function)
gp.init_population()
gp.generation(steps=200)

#gp = read_file(directory='15min/training/gp_04.pkl')
#gp.additional_generation(steps=100)

write_file(directory='15min/training/gp_05.pkl', obj=gp)
