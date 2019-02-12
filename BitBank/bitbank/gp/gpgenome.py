import random
from bitbank.gp.node import Node
from bitbank.exceptions.gpexception import NodeException
import copy
from graphviz import Digraph


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

    def normalization(self):
        """
        正規化。拡張した枝刈り
        :return:
        """
        self.pruning_tree()
        r, rr, sr, er = self.true_route()
        self.pruning_tree_fill(success_route=sr)

    def show_tree_map(self, name):
        g = Digraph(format='png')
        g.attr('node', shape='circle')
        g = self.tree.show_node_map(g)
        print(g)
        g.render(name)

    def pruning_tree(self):
        """
        枝刈り
        :return:
        """
        self.tree.pruning()
        self.update_total()

    def true_route(self):
        """
        葉ノードがTrueのルートを返す
        :return:
        """
        routes = self.tree.true_route(par_route=list(), true_route=list())
        routes = [self.tree.true_route_rl(true_route=route, depth=0) for route in routes]
        tech_list = self.condition.get_tech_list()
        r = list()
        rr = list()
        sr = list()
        er = list()
        for route in routes:
            d = dict()
            n = list()
            for tech in tech_list:
                d[tech] = list()
            for node in route:
                node_id = node['node_id']
                n.append(node_id)
                tech_name = node['tech_name']
                threshold = node['threshold']
                operation = node['operation']
                result = node['result']
                if (operation == Node.MORE_THAN and result) or (operation == Node.LESS_THAN and not result):
                    d[tech_name].append(str('{0:.5f}'.format(threshold)) + ' <')
                elif (operation == Node.LESS_THAN and result) or (operation == Node.MORE_THAN and not result):
                    d[tech_name].append(str('<' + ' {0:.5f}'.format(threshold)))
            r.append(d)
            flag = False
            for i in d:
                if len(d[i]) == 0:
                    flag = True
                    break
            if flag:
                er.append(n)
            else:
                rr.append(d)
                sr.append(n)
        return r, rr, sr, er

    def pruning_tree_fill(self, success_route):
        """
        全ての項目を評価するルートのみにする
        :param success_route:
        :return:
        """
        sr_unique = list()
        for route in success_route:
            sr_unique.extend(route)
        sr_unique = list(set(sr_unique))
        dl_node_id = [i for i in (list(range(self.__total_node + 1))) if not (i in sr_unique)]

        for dl in dl_node_id:
            self.tree.false_node(node_id=dl)
        self.update_total()
