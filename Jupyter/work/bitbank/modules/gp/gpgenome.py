from modules.gp.node import Node


class GPGenome:

    def __init__(self, condition):
        self.condition = condition
        self.tree = Node(condition=condition)
        self.tree.update_id(node_id=0)
