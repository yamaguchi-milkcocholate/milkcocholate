from bitbank.gp.gp import GeneticNetwork
from bitbank.gp.fitnessfunction.tag import TagFitnessFunction
import sys
sys.setrecursionlimit(100000)

fitness_function = TagFitnessFunction(ema_term=4, ma_term=8, goal=0.1)

gp = GeneticNetwork(mutation=5, cross=50, elite_num=1, population=3, fitness_function=fitness_function)
gp.init_population()
gp.generation(steps=10)
