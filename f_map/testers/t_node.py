from f_utils import u_tester
from f_map.c_node import Node


class TestNode:

    def __init__(self):
        u_tester.print_start(__file__)
        TestNode.__tester_ordering()
        u_tester.print_finish(__file__)

    @staticmethod
    def __tester_ordering():
        # F is Infinity
        p0 = Node(x=1, y=2) < Node(x=1, y=3)
        p1 = Node(x=1, y=2) <= Node(x=1, y=2)
        p2 = Node(x=1, y=2) > Node(x=0, y=0)
        p3 = Node(x=1, y=2) >= Node(x=1, y=2)
        # F is equal but G_1 < G_2
        node_1 = Node(x=1, y=1)
        node_1.g = 10
        node_1.h = 90
        node_1.f = 100
        node_2 = Node(x=2, y=2)
        node_2.g = 90
        node_2.h = 10
        node_2.f = 100
        p4 = node_1 > node_2
        # F and G are equal
        node_3 = Node(x=3, y=3)
        node_3.g = 90
        node_2.h = 10
        node_2.f = 100
        p5 = node_2 < node_3
        u_tester.run(p0, p1, p2, p3, p4, p5)


if __name__ == '__main__':
    TestNode()
