from f_data_structure.node_tree import Node


class Tree:

    def __init__(self, root=None):
        self.root = root
        self.nodes = dict()
        if not root:
            self.root = Node(name='root')
        self.nodes[self.root.name] = self.root

    def add(self, node, parent=None):
        if not parent:
            parent = self.nodes['root']
        parent.children.add(node)
        self.nodes[node.name] = node

    @classmethod
    def subtree(cls, node):
        tree = Tree(root=node)
        for child in node.get_descendants():
            tree.nodes[child.name] = child
        return tree
