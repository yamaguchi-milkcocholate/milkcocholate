import sys, os
sys.path.append(os.pardir)
from modules.ga import ga

gaga = ga.GeneticAlgorithm(2, 70, [(1, 2), (1, 2)], 1, 100)

gaga.save_geno_type('data')
