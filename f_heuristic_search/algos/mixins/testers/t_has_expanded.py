from f_heuristic_search.algos.mixins.has_expanded import HasExpanded, NodeBase


def test_has_expanded():
    a = NodeBase('A')
    b = NodeBase('B')
    algo = HasExpanded()
    algo._expanded.add(b)
    algo._expanded.add(a)
    assert algo.expanded == {b, a}
