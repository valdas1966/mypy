from f_graph.path.elements.node import NodePath as Node


def test_key_comparison():
    a = Node(uid='a', h=0)
    b = Node(uid='b', h=0)
    assert a < b
