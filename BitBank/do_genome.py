from bitbank.gp.gp import GeneticNetwork
from bitbank.functions import read_file
import sys
from pprint import pprint
sys.setrecursionlimit(100000)

gp = read_file(directory='15min/training/gp_02.pkl')
genome = gp.get_elite_genome()
r, rr, sr, er = genome.true_route()
genome.pruning_true_route(success_route=sr, keep=3, depth=10)
genome.show_tree_map(name='genome_tree_2')
