from modules.gn.node import Node


class GNGenome:

    def __init__(self, condition):
        self.condition = condition
        self.tree = Node(condition=condition)
