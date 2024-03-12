from f_heuristic_search.nodes.i_3_f_cell import Node


def test_node():
    n = Node()
    assert str(n) == '(0,0)[g=0, h=None, f=None]'
