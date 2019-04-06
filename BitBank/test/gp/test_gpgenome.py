import sys
import os
import unittest
sys.path.append(os.pardir + '/../')
from bitbank.gp.gpgenome import GPGenome
from bitbank.gp.condition import Condition
from bitbank.gp.node import Node


class TestGPGenome(unittest.TestCase):

    def setUp(self):
        condition = Condition()
        condition.add_technical_analysis(
            name='ma_ema',
            lower_limit=-0.1,
            upper_limit=0.1
        )
        condition.add_technical_analysis(
            name='price_ema',
            lower_limit=-0.1,
            upper_limit=0.1
        )
        self.genome = GPGenome(condition=condition)
        self.condition = condition

    def test_add_node(self):
        self.genome.show_tree()
        pass

    def test_put_node(self):
        node = self.genome.random_node()
        node_id = node.node_id

        total = self.genome.get_total()
        # 全てのノードを取り出しできるか
        for i in range(total):
            node_r = self.genome.get_node(node_id=i)

        # 全てのノードを置き換えられるか
        # ルートは取れない
        for i in range(1, total):
            new_node = Node(condition=self.condition)
            self.genome.put_node(new_node, i)

        # 突然変異
        for i in range(total):
            self.genome.tree.mutate(node_id=i, condition=self.condition)

    def test_operation(self):
        r = self.genome.operation(
            price_ema=0.1,
            ma_ema=0.1
        )
        print(r)


if __name__ == '__main__':
    unittest.main()
