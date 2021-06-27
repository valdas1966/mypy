from f_data_structure.tree import Tree
from f_data_structure.node_tree import Node
from f_utils import u_tester


class TestTree:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_init()
        self.__tester_add()
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
        tree.add(node, parent='root')
        names_true = {'root', 'a'}
        p0 = {n.name for n in tree.nodes.values()} == names_true
        p1 = tree.nodes['root'].children = {node}
        p2 = tree.nodes['a'].parent = tree.nodes['root']
        u_tester.run(p0, p1, p2)


if __name__ == '__main__':
    TestTree()
