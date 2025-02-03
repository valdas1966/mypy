from f_graph.path.one_to_one.algos.generators.g_a_star import GenAStar


def test_3x3() -> None:
    """
    ========================================================================
     Test A* algorithm on a 3x3 grid graph.
    ========================================================================
    """
    a_star = GenAStar.gen_3x3()
    solution = a_star.run()
    graph = a_star._problem.graph
    path_true = [graph[0, 0], graph[0, 1], graph[0, 2],
                 graph[1, 2], graph[2, 2]]
    assert solution.path == path_true
    assert list(solution.state.generated) == [graph[1, 1], graph[1, 0]]
    assert solution.stats.generated == 7
    assert solution.state.explored == {graph[0, 0], graph[0, 1], graph[0, 2],
                                       graph[1, 2]}
    assert solution.stats.explored == 4
    assert solution.state.best == graph[2, 2]


def test_3x3_cache() -> None:
    """
    ========================================================================
     Test A* algorithm on a 3x3 grid graph with cache.
    ========================================================================
    """
    a_star = GenAStar.gen_3x3_cache()
    solution = a_star.run()
    graph = a_star._problem.graph
    path_true = [graph[0, 0], graph[0, 1], graph[0, 2],
                 graph[1, 2], graph[2, 2]]
    assert solution.path == path_true
    assert list(solution.state.generated) == [graph[1, 0]]
    assert solution.stats.generated == 3
    assert solution.state.explored == {graph[0, 0]}
    assert solution.stats.explored == 1
    assert solution.state.best == graph[0, 1]
