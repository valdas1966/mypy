from f_data_structure.nodes.node_2_g import NodeG


def test_g():
    a = NodeG()
    assert a.g == 0
    b = NodeG(parent=a)
    assert b.g == 1
    c = NodeG(parent=a)
    assert c.g == 1
    b.parent = c
    assert b.g == 2
    b.parent = None
    assert b.g == 0


def test_sort():
    a = NodeG()
    assert a >= a
    b = NodeG()
    assert a >= b
    c = NodeG(parent=a)
    assert c < a
    assert b > c
