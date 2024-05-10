from f_hs.nodes.i_2_f import NodeF


def test_f():
    a = NodeF()
    a.h = 1
    b = NodeF(parent=a)
    b.h = 0
    assert a.f() == 1
    assert b.f() == 1
