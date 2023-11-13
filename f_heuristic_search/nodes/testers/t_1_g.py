from f_heuristic_search.nodes.i_1_g import NodeG


def test_start():
    node = NodeG()
    assert node.g == 0


def test_parent():
    a = NodeG()
    b = NodeG(parent=a)
    assert b.g == 1


def test_is_better_parent():
    a = NodeG()
    a._g = 2
    b = NodeG()
    b._g = 3
    c = NodeG(parent=b)
    assert c.is_better_parent(a)

    