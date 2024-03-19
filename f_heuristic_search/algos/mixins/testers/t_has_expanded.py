from f_heuristic_search.algos.mixins.has_expanded import HasExpanded, NodeBase as Node


def test_has_expanded():
    a = Node('A')
    b = Node('B')
    algo = HasExpanded[Node]()
    algo._expanded.add(b)
    algo._expanded.add(a)
    assert algo.expanded == {b, a}
