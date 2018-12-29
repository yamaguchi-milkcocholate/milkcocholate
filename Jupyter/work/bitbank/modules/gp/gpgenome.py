import random
from modules.gp.node import Node


class GPGenome:

    def __init__(self, condition):
        self.condition = condition
        self.tree = Node(condition=condition)
        self.__total_node = None
        self.update_total()

    def show_tree(self):
        """
        木構造を表示
        """
        self.tree.show_node()

    def update_total(self):
        """
        ノード数を返す(0~)
        """
        self.__total_node = self.tree.update_id(node_id=0)

    def get_total(self):
        """
        ノード数を返す
        :return: integer
        """
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
        """
        ノードを差し替える
        :param node:    Node
        :param node_id: integer
        """
        if not self.tree.put_node(node=node, node_id=node_id):
            raise Exception('not found')
        self.update_total()

    def mutate(self):
        node_id = random.randint(0, self.__total_node)
        if not self.tree.mutate(node_id=node_id, condition=self.condition):
            raise Exception('not found')
