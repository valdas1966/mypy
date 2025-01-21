from f_graph.path.one_to_one.generators.g_cache import GenCache
from f_graph.path.one_to_one.generators.g_problem import GenProblemOneToOne


def test_gen_3x3() -> None:
    """
    ========================================================================
     Test that gen_3x3 creates a cache for a 3x3 problem.
    ========================================================================
    """
    cache = GenCache.gen_3x3()
    problem = GenProblemOneToOne.gen_3x3()
    goal = problem.graph[0, 2]
    best = problem.graph[0, 1]
    assert cache[goal]() == []
    assert cache[best]() == [goal]
