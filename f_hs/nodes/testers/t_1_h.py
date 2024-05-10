from f_hs.nodes.i_1_h import NodeH


def test_h():
    a = NodeH()
    a.h = 1
    b = NodeH()
    b.h = 2
    assert a < b
