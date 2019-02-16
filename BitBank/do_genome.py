from bitbank.gp.gp import GeneticNetwork
from bitbank.functions import read_file
import sys
from pprint import pprint
sys.setrecursionlimit(100000)

gp = read_file(directory='15min/training/gp_03.pkl')
genome = gp.get_elite_genome()
genome.show_tree_map(name='genome_tree_3')
