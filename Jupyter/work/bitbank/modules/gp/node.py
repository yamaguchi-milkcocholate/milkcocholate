import random


class Node:
    MORE_THAN = 100
    LESS_THAN = 200
    EON = 300
    MAX_DEPTH = 4

    def __init__(self, condition, depth=0):
        self.tech_name = None
        self.threshold = None
        self.operation = None
        self.left_node = None
        self.right_node = None
        self.node_id = None
        self.depth = depth
        self.__new(condition=condition)

    def __new(self, condition):
        """
        このノードのテクニカル分析指標を決定する
        :param condition: Condition
        """
        tech_analysis = condition.random_choice()
        self.tech_name = tech_analysis['name']
        self.threshold = random.uniform(tech_analysis['lower_limit'], tech_analysis['upper_limit'])
        if random.randint(0, 9) % 2 == 0:
            self.operation = self.MORE_THAN
        else:
            self.operation = self.LESS_THAN
        if self.depth <= self.MAX_DEPTH:
            # 1/5でEON
            if random.randint(1, 100) % 5 == 0:
                self.left_node = self.EON
            else:
                self.left_node = Node(condition=condition, depth=self.depth + 1)
            if random.randint(1, 100) % 5 == 0:
                self.right_node = self.EON
            else:
                self.right_node = Node(condition=condition, depth=self.depth + 1)
        else:
            self.left_node = self.EON
            self.right_node = self.EON

    def show_node(self):
        print('depth: ' + str(self.depth), self.tech_name, self.threshold, self.operation, self.node_id)
        self.__line_branch()
        if self.left_node == self.EON:
            print('EON')
        else:
            self.left_node.show_node()
        self.__line_branch()
        if self.right_node == self.EON:
            print('EON')
        else:
            self.right_node.show_node()

    def __line_branch(self):
        for i in range(self.depth + 1):
            print('--', end='')

    def update_id(self, node_id):
        """
        ノードIDを更新
        :param node_id: integer
        :return: integer 自分のIDを返す
        """
        self.node_id = node_id
        if isinstance(self.left_node, Node):
            node_id = self.left_node.update_id(node_id=node_id + 1)
        if isinstance(self.right_node, Node):
            node_id = self.right_node.update_id(node_id=node_id + 1)
        return node_id

    def get_node(self, node_id):
        if node_id == self.node_id:
            return self.node_id
        else:
            # False or node_id
            right = self.__get_right_node(node_id=node_id)
            left = self.__get_left_node(node_id=node_id)
            # 答えがあれば答えを、なければFalseを返す
            if right:
                # 右側に答えがあった
                return right
            elif left:
                # 左側に答えがあった
                return left
            else:
                # 両方とも答えがなかった
                return False

    def __get_right_node(self, node_id):
        """
        右側のノートに問い合わせる
        :param node_id:
        :return:
        """
        if isinstance(self.left_node, Node):
            result = self.left_node.get_node(node_id=node_id)
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
