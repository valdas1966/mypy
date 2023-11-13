from f_heuristic_search.nodes.i_2_f import NodeF


def test_ghf():
    a = NodeF(h=1)
    b = NodeF(h=1, parent=a)
    assert a.h == 1
    assert b.g == 1
    assert b.f() == 2


def test_cost():
    a = NodeF(h=1)
    b = NodeF(h=2)
    a._g = 2
    b._g = 1
    assert a.f() == 3
    assert b.f() == 3
    assert not a == b
    assert a < b
