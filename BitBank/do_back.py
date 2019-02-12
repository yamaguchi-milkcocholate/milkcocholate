from bitbank.gp.gp import GeneticNetwork
from bitbank.gp.fitnessfunction.tag import TagFitnessFunction
import sys
from bitbank.functions import write_file
sys.setrecursionlimit(100000)

fitness_function = TagFitnessFunction(ema_term=4, ma_term=8, goal=0.15)

gp = GeneticNetwork(mutation=5, cross=50, elite_num=2, population=75, fitness_function=fitness_function)
gp.init_population()
gp.generation(steps=200)

write_file(directory='15min/training/gp_02.pkl', obj=gp)
