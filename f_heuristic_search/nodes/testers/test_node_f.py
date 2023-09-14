from f_heuristic_search.nodes.node_3_f import NodeF


def test_f():
    start = NodeF(name='start', h=2)
    assert start.f() == 2
    a = NodeF(name='a', parent=start, h=1)
    assert a.f() == 2
    b = NodeF(name='b', parent=start, h=2)
    assert b.f() == 3
    c = NodeF(name='c', parent=b, h=1)
    assert c.f() == 3
    goal = NodeF(name='goal', parent=a, h=0)
    assert goal.f() == 2
    assert goal < a < start < c < b
    goal.parent = c
    assert goal.f() == 3
