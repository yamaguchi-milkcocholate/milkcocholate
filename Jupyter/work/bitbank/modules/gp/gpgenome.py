import random
from modules.gp.node import Node


class GPGenome:

    def __init__(self, condition):
        self.condition = condition
        self.tree = Node(condition=condition)
        self.__total_node = None
        self.update_total()

    def show_tree(self):
        self.tree.show_node()

    def update_total(self):
        """
        ノード数を返す(0~)
        """
        self.__total_node = self.tree.update_id(node_id=0)

    def get_total(self):
        return self.__total_node

    def random_node(self):
        """
        ランダムなノードを返す
        :return: Node
        """
        result = self.tree.get_node(node_id=(random.randint(0, self.__total_node)))
        if not result:
            raise Exception('not found')
        return result

    def put_node(self, node, node_id):
        if not self.tree.put_node(node=node, node_id=node_id):
            raise Exception('not found')
