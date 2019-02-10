import random
from bitbank.gp.node import Node
from bitbank.exceptions.gpexception import NodeException
import copy


class GPGenome:

    def __init__(self, condition):
        self.condition = condition
        self.tree = Node(condition=condition)
        self.__total_node = None
        self.update_total()

    def operation(self, **kwargs):
        tech_list = kwargs.keys()
        for tech_name in tech_list:
            if not (tech_name in self.condition.get_tech_list()):
                raise Exception('tech name not found')
        try:
            result = self.tree.pass_nodes(kwargs)
        except AttributeError as e:
            print(kwargs)
            self.show_tree()
            raise e
        return result

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
        ids = random.randint(1, self.__total_node)
        result = self.tree.get_node(node_id=ids)
        if not result:
            self.show_tree()
            print(ids)
            raise Exception('not found')
        return copy.deepcopy(result)

    def get_node(self, node_id):
        """
        ノードを指定して返す
        :param node_id:
        :return:
        """
        result = self.tree.get_node(node_id=node_id)
        if not result:
            raise Exception('not found')
        return copy.deepcopy(result)

    def put_node(self, node, node_id):
        """
        ノードを差し替える
        ルートは差し替えられない
        :param node:    Node
        :param node_id: integer(not 0)
        """
        if not self.tree.put_node(node=node, node_id=node_id):
            raise NodeException('put_node: not found')
        self.update_total()

    def mutate(self):
        node_id = random.randint(1, self.__total_node)
        if not self.tree.mutate(node_id=node_id, condition=self.condition):
            raise NodeException('mutate: not found\nnode_id: ' + str(node_id))
