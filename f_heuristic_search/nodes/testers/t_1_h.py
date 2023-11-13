from f_heuristic_search.nodes.i_1_h import NodeH


def test_h():
    a = NodeH(h=1)
    b = NodeH()
    b.h = 2
    assert a < b
