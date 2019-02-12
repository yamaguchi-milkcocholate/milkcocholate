import random
import copy


class Node:
    MORE_THAN = 100
    LESS_THAN = 200
    EON = 300
    MAX_DEPTH = 20
    LEAF = 5
    LEAF_OPERATION = 'operation'

    def __init__(self, condition, depth=0):
        self.tech_name = None
        self.threshold = None
        self.operation = None
        self.left_node = None
        self.right_node = None
        self.node_id = None
        self.depth = depth
        self.__new(condition=condition)

    def pass_nodes(self, tech_names):
        """
        演算比較を行いYes, Noを返す
        :param tech_names:
        :return:
        """
        if self.tech_name == self.LEAF_OPERATION:
            return self.operation
        else:
            if self.judge(tech_names=tech_names):
                return self.left_node.pass_nodes(tech_names=tech_names)
            else:
                return self.right_node.pass_nodes(tech_names=tech_names)

    def judge(self, tech_names):
        """
        満たしていればTrueで左
        満たしていなければFalseで右
        :param tech_names:
        :return:
        """
        v = float(tech_names[self.tech_name])
        if self.MORE_THAN == self.operation:
            if v > self.threshold:
                return True
            else:
                return False
        elif self.LESS_THAN == self.operation:
            if v < self.threshold:
                return True
            else:
                return False

    def __new(self, condition):
        """
        このノードのテクニカル分析指標を決定する
        :param condition: Condition
        """
        if self.depth <= self.MAX_DEPTH:
            # 1/5でEON
            if random.randint(1, 100) % self.LEAF == 0 and self.depth != 0:
                self.random_operation()
            else:
                # テクニカル指標を割り当て
                self.random_tech_analysis(condition=condition)
                self.left_node = Node(condition=condition, depth=self.depth + 1)
                self.right_node = Node(condition=condition, depth=self.depth + 1)
        else:
            self.random_operation()

    def random_operation(self):
        """
        葉ノードにYes, Noを割り当てる
        :return:
        """
        if random.randint(1, 100) % 2 == 0:
            self.operation = True
        else:
            self.operation = False
        self.left_node = self.EON
        self.right_node = self.EON
        self.threshold = None
        self.tech_name = 'operation'

    def show_node(self):
        print('depth:', str(self.depth), 'node_id: ', self.node_id, self.tech_name, self.threshold, self.operation)
        if self.left_node == self.EON:
            pass
        else:
            self.__line_branch()
            self.left_node.show_node()
        if self.right_node == self.EON:
            pass
        else:
            self.__line_branch()
            self.right_node.show_node()

    def __line_branch(self):
        for i in range(self.depth + 1):
            print('--', end='')

    def update_id(self, node_id, depth=0):
        """
        ノードIDを更新
        :param node_id: integer
        :param depth: integer
        :return: integer 自分のIDを返す
        """
        self.node_id = node_id
        self.depth = depth
        if isinstance(self.left_node, Node):
            node_id = self.left_node.update_id(node_id=node_id + 1, depth=depth + 1)
        if isinstance(self.right_node, Node):
            node_id = self.right_node.update_id(node_id=node_id + 1, depth=depth + 1)
        return node_id

    def false_node(self, node_id):
        """
        Falseの葉ノードに変更
        :param node_id:
        :return:
        """
        if node_id == self.node_id:
            self.left_node = self.EON
            self.right_node = self.EON
            self.tech_name = self.LEAF_OPERATION
            self.threshold = None
            self.operation = False
        else:
            if isinstance(self.right_node, Node):
                self.right_node.false_node(node_id=node_id)
            if isinstance(self.left_node, Node):
                self.left_node.false_node(node_id=node_id)

    def get_node(self, node_id):
        """
        :param node_id:
        :return:
        """
        if node_id == self.node_id:
            return copy.deepcopy(self)
        else:
            # False or node_id
            right = self.__get_right_node(node_id=node_id)
            # 答えがあれば答えを、なければFalseを返す
            if right:
                # 右側に答えがあった
                return right

            # False or node_id
            left = self.__get_left_node(node_id=node_id)
            if left:
                # 左側に答えがあった
                return left
            # 両方とも答えがなかった
            return False

    def __get_right_node(self, node_id):
        """
        右側のノートに問い合わせる
        :param node_id:
        :return:
        """
        if isinstance(self.right_node, Node):
            result = self.right_node.get_node(node_id=node_id)
        else:
            result = False
        return result

    def __get_left_node(self, node_id):
        """
        左側のノードに問い合わせる
        :param node_id:
        :return:
        """
        if isinstance(self.left_node, Node):
            result = self.left_node.get_node(node_id=node_id)
        else:
            result = False
        return result

    def put_node(self, node, node_id):
        """
        子ノードを調べて、IDが一致すればノードを入れ替える
        :param node:    差し替えるノード
        :param node_id: 対象のID
        :return: bool 見つかったかどうか
        """
        # まずは右のノードから調べる

        if isinstance(self.right_node, Node):
            if self.right_node.get_node_id() == node_id:
                # 正解なら入れ替えてTrue
                self.right_node = node
                return True
            else:
                # 失敗ならノードに調べさせる
                if self.right_node.put_node(node=node, node_id=node_id):
                    return True
                else:
                    pass
        # ノードがないならFalse
        else:
            pass

        # 右のノードで見つからなかったら、次は左ノード

        if isinstance(self.left_node, Node):
            if self.left_node.get_node_id() == node_id:
                # 正解なら入れ替えてTrue
                self.left_node = node
                return True
            else:
                # 失敗ならノードに調べさせる
                if self.left_node.put_node(node=node, node_id=node_id):
                    return True
                else:
                    pass
        else:
            pass

        # このノードにはない
        return False

    def mutate(self, node_id, condition):
        """
        突然変異を起こす
        違ければ、子ノードを調べる
        :param node_id:   integer
        :param condition: Condition
        :return: bool
        """
        if node_id == self.node_id:
            if self.tech_name != self.LEAF_OPERATION:
                self.random_tech_analysis(condition=condition)
            return True
        else:
            right = self.__mutate_right_node(node_id=node_id, condition=condition)
            # 答えがあれば答えを、なければFalseを返す
            if right:
                # 右側に答えがあった
                return right

            left = self.__mutate_left_node(node_id=node_id, condition=condition)
            if left:
                # 左側に答えがあった
                return left

            # 両方とも答えがなかった
            return False

    def random_tech_analysis(self, condition):
        tech_analysis = condition.random_choice()
        self.tech_name = tech_analysis['name']
        self.threshold = random.uniform(tech_analysis['lower_limit'], tech_analysis['upper_limit'])
        if random.randint(0, 9) % 2 == 0:
            self.operation = self.MORE_THAN
        else:
            self.operation = self.LESS_THAN

    def __mutate_right_node(self, node_id, condition):
        """
        右ノードを調べて突然変異を起こす
        :param node_id:
        :param condition:
        :return: bool
        """
        if isinstance(self.right_node, Node):
            result = self.right_node.mutate(node_id=node_id, condition=condition)
        else:
            result = False
        return result

    def __mutate_left_node(self, node_id, condition):
        """
        左ノードを調べて突然変異を起こす
        :param node_id:
        :param condition:
        :return: bool
        """
        if isinstance(self.left_node, Node):
            result = self.left_node.mutate(node_id=node_id, condition=condition)
        else:
            result = False
        return result

    def show_node_map(self, g, par_node_id=None):
        """
        木構造の可視化
        :param g:
        :param par_node_id:
        :return:
        """
        g.node(str(self.node_id), self.__node_map())
        if par_node_id is None:
            pass
        else:
            g.edge(str(par_node_id), str(self.node_id))

        if isinstance(self.right_node, Node):
            g = self.right_node.show_node_map(g, par_node_id=self.node_id)

        if isinstance(self.left_node, Node):
            g = self.left_node.show_node_map(g, par_node_id=self.node_id)

        return g

    def __node_map(self):
        """
        ノードの基準を文字列にする
        :return:
        """
        if self.tech_name == self.LEAF_OPERATION:
            return str(self.operation)
        else:
            if self.operation == self.MORE_THAN:
                operation = '>'
            else:
                operation = '<'
            return self.tech_name + " " + operation + " {0:.5f}".format(self.threshold)

    def pruning(self):
        """
        枝刈り
        :return:
        """
        if self.left_node != self.EON and self.right_node != self.EON:
            left_tech_name = self.left_node.get_tech_name()
            right_tech_name = self.right_node.get_tech_name()
            if left_tech_name == self.LEAF_OPERATION and right_tech_name == self.LEAF_OPERATION:
                left_operation = self.left_node.get_operation()
                right_operation = self.right_node.get_operation()
                if left_operation == right_operation:
                    self.__end_of_node(operation=left_operation)
            else:
                if isinstance(self.left_node, Node):
                    self.left_node.pruning()
                if isinstance(self.right_node, Node):
                    self.right_node.pruning()

    def __end_of_node(self, operation):
        """
        葉ノードに変更する
        :param operation:
        :return:
        """
        self.right_node = self.EON
        self.left_node = self.EON
        self.operation = operation
        self.threshold = None
        self.tech_name = self.LEAF_OPERATION

    def true_route(self, par_route, true_route):
        """
        葉ノードがTrueのルートを返す
        :param par_route: list
        :param true_route: list
        :return:
        """
        par_route.append({
            'node_id': self.node_id,
            'tech_name': self.tech_name,
            'threshold': self.threshold,
            'operation': self.operation
        })
        if self.tech_name == self.LEAF_OPERATION:
            if self.operation:
                true_route.append(list(par_route))

        if isinstance(self.left_node, Node):
            true_route = self.left_node.true_route(par_route=list(par_route), true_route=list(true_route))
        if isinstance(self.right_node, Node):
            true_route = self.right_node.true_route(par_route=list(par_route), true_route=list(true_route))

        return true_route

    def true_route_rl(self, true_route, depth):
        """
        ルートの左右を付け加える
        :param true_route:
        :param depth:
        :return:
        """
        if depth < len(true_route) - 1:
            next_node_id = true_route[depth + 1]['node_id']
            left_node_id = self.left_node.get_node_id()
            right_node_id = self.right_node.get_node_id()
            # 左はTrue
            if next_node_id == left_node_id:
                true_route[depth]['result'] = True
                true_route = self.left_node.true_route_rl(true_route=true_route, depth=depth + 1)
            elif next_node_id == right_node_id:
                true_route[depth]['result'] = False
                true_route = self.right_node.true_route_rl(true_route=true_route, depth=depth + 1)
            return true_route
        else:
            true_route[depth]['result'] = None
            return true_route

    def get_operation(self):
        """
        :return:
        """
        return self.operation

    def get_tech_name(self):
        """
        :return:
        """
        return self.tech_name

    def get_node_id(self):
        """
        :return:
        """
        return self.node_id

    def get_right_node(self):
        """
        :return:
        """
        return self.right_node

    def get_left_node(self):
        """
        :return:
        """
        return self.left_node

    def set_right_node(self, node):
        """
        :param node:
        :return:
        """
        self.right_node = node

    def set_left_node(self, node):
        """
        :param node:
        :return:
        """
        self.left_node = node

    def set_operation(self, operation):
        """
        :param operation:
        :return:
        """
        self.operation = operation

    def set_threshold(self, threshold):
        """
        :param threshold:
        :return:
        """
        self.threshold = threshold

    def set_tech_name(self, tech_name):
        """
        :param tech_name:
        :return:
        """
        self.tech_name = tech_name
