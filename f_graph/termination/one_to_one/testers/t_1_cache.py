from f_graph.termination.one_to_one.i_1_cache import TerminationCache, NodePath

goal = NodePath(name='GOAL')
node = NodePath(name='NODE')


def test_cache():
    t = TerminationCache(goal=goal, cache={node})
    assert t.can(node=goal)
    assert t.can(node=node)
