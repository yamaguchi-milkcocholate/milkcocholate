import random
import numpy as np
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
        try:
            ids = random.randint(1, self.__total_node)
        except ValueError:
            ids = 0
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
        if node_id == 0:
            self.tree = node
        else:
            if not self.tree.put_node(node=node, node_id=node_id):
                raise NodeException('put_node: not found')
        self.update_total()

    def mutate(self):
        try:
            node_id = random.randint(1, self.__total_node)
        except ValueError:
            node_id = 0
        if not self.tree.mutate(node_id=node_id, condition=self.condition):
            raise NodeException('mutate: not found\nnode_id: ' + str(node_id))

    def normalization(self, keep, depth):
        """
        正規化。拡張した枝刈り
        :param keep:
        :param depth:
        :return:
        """
        self.pruning_tree()
        r, rr, sr, er = self.true_route()
        self.pruning_tree_fill(success_route=sr)
        r, rr, sr, er = self.true_route()
        self.pruning_true_route(success_route=sr, keep=keep, depth=depth)

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

    def pruning_true_route(self, success_route, keep, depth):
        """
        ルートを少なくする
        1. 深さを超えるルートを削除
        2. 残ったルートからさらに減らす
        :param success_route:
        :param keep: 残すルートの数
        :param depth: 深さ
        :return:
        """
        route_num = len(success_route)
        exceed = [i for i in range(route_num) if len(success_route[i]) > depth]

        # 削除しないルートのNODE ID
        rem_r = [success_route[i] for i in range(route_num) if not (i in exceed)]
        rem_r = [flatten for inner in rem_r for flatten in inner]
        rem_r = list(set(rem_r))
        # 削除するルートのNODE ID
        del_r = [success_route[i] for i in range(route_num) if i in exceed]
        del_r = [flatten for inner in del_r for flatten in inner]
        del_r = list(set(del_r))

        # 削除するNODE ID
        del_n = [i for i in del_r if not (i in rem_r)]

        for dl in del_n:
            self.tree.false_node(node_id=dl)

        success_route = [success_route[i] for i in range(route_num) if len(success_route[i]) <= depth]
        route_num -= len(exceed)
        del_num = route_num - keep
        series = np.arange(0, route_num)
        if del_num > 0:
            # 削除するルートのインデックス
            select = np.random.choice(series, del_num, False)
            # 削除しないルートのNODE ID
            rem_r = [success_route[i] for i in range(route_num) if not (i in select)]
            rem_r = [flatten for inner in rem_r for flatten in inner]
            rem_r = list(set(rem_r))
            # 削除するルートのNODE ID
            del_r = [success_route[i] for i in range(route_num) if i in select]
            del_r = [flatten for inner in del_r for flatten in inner]
            del_r = list(set(del_r))

            # 削除するNODE ID
            del_n = [i for i in del_r if not (i in rem_r)]

            for dl in del_n:
                self.tree.false_node(node_id=dl)
        self.update_total()
