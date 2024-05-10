from f_hs.nodes.i_1_g import NodeG


def test_start():
    node = NodeG()
    assert node.g == 0


def test_parent():
    a = NodeG()
    b = NodeG(parent=a)
    assert b.g == 1


def test_update_parent():
    a = NodeG(name='a')
    a._g = 10
    b = NodeG(name='b')
    b._g = 5
    c = NodeG(name='c', parent=a)
    c.update_parent_if_needed(parent=c)
    assert c.parent == a
    c.update_parent_if_needed(parent=b)
    assert c.parent == b
    