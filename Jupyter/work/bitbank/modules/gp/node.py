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
        print('depth: ' + str(self.depth), self.tech_name, self.threshold, self.operation)
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
