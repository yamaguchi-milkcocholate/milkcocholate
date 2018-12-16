import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from modules.gn.gngenome import GNGenome
from modules.gn.condition import Condition


class TestGNGenome(unittest.TestCase):

    def setUp(self):
        condition = Condition()
        condition.add_technical_analysis(
            name='bollingerband',
            lower_limit=0,
            upper_limit=100
        )
        condition.add_technical_analysis(
            name='rsi',
            lower_limit=0.3,
            upper_limit=0.5
        )
        self.genome = GNGenome(condition=condition)

    def test_add_node(self):
        self.genome.tree.show_node()


if __name__ == '__main__':
    unittest.main()
