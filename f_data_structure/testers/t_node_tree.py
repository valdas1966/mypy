from f_data_structure.node_tree import Node
from f_utils import u_tester


class TestNodeTree:

    def __init__(self):
        u_tester.print_start(__file__)
        self.__tester_init()
        self.__tester_get_descendants()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_init():
        node = Node(name='a', data=None)
        p0 = node.name == 'a'
        u_tester.run(p0)

    @staticmethod
    def __tester_add():
        node_a = Node(name='a')
        node_b = Node(name='b')
        node_c = Node(name='c')
        node_d = Node(name='d')
        node_e = Node(name='e')
        node_a.add(node_b)
        node_a.add(node_c)
        node_c.add(node_d)
        node_c.add(node_e)
        p0 = node_a.children == {node_b, node_c}
        p1 = node_b.children == set()
        p2 = node_c.children == {node_d, node_e}
        u_tester.run(p0, p1, p2)

    @staticmethod
    def __tester_get_descendants():
        node_a = Node(name='a')
        node_b = Node(name='b')
        node_c = Node(name='c')
        node_d = Node(name='d')
        node_e = Node(name='e')
        node_a.children.add(node_b)
        node_a.children.add(node_c)
        node_c.children.add(node_d)
        node_c.children.add(node_e)
        descendants_true = ['a', 'b', 'c', 'd', 'e']
        p0 = [n.name for n in node_a.get_descendants()] == descendants_true
        p1 = [n.name for n in node_b.get_descendants()] == ['b']
        u_tester.run(p0, p1)


if __name__ == '__main__':
    TestNodeTree()
