from f_heuristic_search.nodes.node_g import NodeG


def test_init_default():
    node = NodeG(x=1, y=2, name='A')
    assert node.x == 1
    assert node.y == 2
    assert node.name == 'A'
    assert node.w == 1
    assert node.g == 0
    assert node.parent is None


def test_update_father():
    node_1 = NodeG(x=1, y=2)
    node_2 = NodeG(x=1, y=3, parent=node_1)
    node_3 = NodeG(x=1, y=4, parent=node_2)
    assert node_3.parent == node_2
    assert node_3.g == 2
    node_4 = NodeG(x=0, y=4)
    node_3.parent = node_4
    assert node_3.parent == node_4
    assert node_3.g == 1
