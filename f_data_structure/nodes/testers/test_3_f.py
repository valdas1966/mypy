from f_data_structure.nodes.node_3_f import NodeF


def test_f():
    """
    ============================================================================
     start(g=0, h=2, f=2) => a(g=1, h=1, f=2) => goal(g=2, h=0, f=2)
     start(g=0, h=2, f=2) => b(g=1, h=2, f=3) => c(g=2, h=1, f=3)
    ============================================================================
    """
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
