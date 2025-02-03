from f_graph.path.generators.g_cache import GenCache, GenProblemOneToOne


def test_gen_3x3():
    """
    ============================================================================
     Test gen_3x3() method.
    ============================================================================
    """
    cache = GenCache.gen_3x3()
    problem = GenProblemOneToOne.gen_3x3()
    graph = problem.graph
    node = graph[0, 1]
    assert cache[node].path() == [graph[0, 2], graph[1, 2], graph[2, 2]]
    assert cache[node].distance() == 3
    