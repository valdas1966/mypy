from f_graph.elements.node import NodeGraph as Node


def test_key_comparison():
    a = Node(uid=1)
    b = Node(uid=2)
    assert a < b
