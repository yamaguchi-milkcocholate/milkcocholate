from bitbank.gp.gp import GeneticNetwork
from bitbank.functions import read_file
import sys
from pprint import pprint
sys.setrecursionlimit(100000)

gp = read_file(directory='15min/training/gp_01.pkl')
genome = gp.get_elite_genome()
genome.show_tree_map(name='genome_tree')

genome.pruning_tree()
genome.show_tree_map(name='genome_tree_p')

route, r_route, sr, er = genome.true_route()

genome.pruning_tree_fill(success_route=sr)
genome.show_tree_map(name='genome_tree_f')
