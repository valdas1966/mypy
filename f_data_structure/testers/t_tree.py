from f_data_structure.tree import Tree
from f_data_structure.node_tree import Node
from f_utils import u_tester


class TestTree:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_init()
        self.__tester_add()
        self.__tester_subtree()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_init():
        tree = Tree()
        nodes_true = {'root': Node(name='root', data=None)}
        p0 = tree.nodes == nodes_true
        u_tester.run(p0)

    @staticmethod
    def __tester_add():
        tree = Tree()
        node = Node(name='a', data=None)
        tree.add(node)
        names_true = {'root', 'a'}
        p0 = {n.name for n in tree.nodes.values()} == names_true
        p1 = tree.nodes['root'].children = {node}
        p2 = tree.nodes['a'].parent = tree.nodes['root']
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_subtree():
        node_a = Node('a')
        node_b = Node('b')
        node_c = Node('c')
        tree = Tree(node_a)
        tree.add(node=node_b, parent=node_a)
        tree.add(node=node_c, parent=node_b)
        subtree = tree.subtree(node_a)
        nodes_true = {'a': node_a, 'b': node_b, 'c': node_c}
        p0 = subtree.nodes == nodes_true
        subtree = tree.subtree(node_b)
        nodes_true = {'b': node_b, 'c': node_c}
        p1 = subtree.nodes == nodes_true
        subtree = tree.subtree(node_c)
        nodes_true = {'c': node_c}
        p2 = subtree.nodes == nodes_true
        u_tester.run(p0, p1, p2)


if __name__ == '__main__':
    TestTree()
