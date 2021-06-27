from f_data_structure.node_tree import Node


class Tree:

    def __init__(self, root=None):
        self.root = root
        self.nodes = dict()
        if not root:
            self.root = Node(name='root', data=None)
        self.nodes[self.root.name] = self.root

    def add(self, node, parent=None):
        if not parent:
            parent = self.nodes['root']
        if type(parent) == str:
            parent = self.nodes[parent]
        node.set_depth(parent.depth + 1)
        parent.add(node)
        self.nodes[node.name] = node
