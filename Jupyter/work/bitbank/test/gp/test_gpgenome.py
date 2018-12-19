import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from modules.gp.gpgenome import GPGenome
from modules.gp.condition import Condition


class TestGPGenome(unittest.TestCase):

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
        self.genome = GPGenome(condition=condition)

    def test_add_node(self):
        self.genome.show_tree()


if __name__ == '__main__':
    unittest.main()
