from f_heuristic_search.domain.grid.node import Node


def test_node():
    n = Node()
    assert str(n) == '(0,0)[g=0, h=None, f=None]'
