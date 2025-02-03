from f_graph.path.one_to_one.algos.generators.g_bfs import GenBFS


def test_3x3() -> None:
    """
    ========================================================================
     Test BFS algorithm on a 3x3 grid graph.
    ========================================================================
    """
    bfs = GenBFS.gen_3x3()
    solution = bfs.run()
    graph = bfs._problem.graph
    path_true = [graph[0, 0], graph[0, 1], graph[0, 2],
                 graph[1, 2], graph[2, 2]]
    assert solution.path == path_true
    assert not solution.state.generated
    assert solution.stats.generated == 9
    assert solution.state.explored == {graph[0, 0], graph[0, 1], graph[0, 2],
                                       graph[1, 0], graph[1, 1], graph[1, 2],
                                       graph[2, 0], graph[2, 1]}
    assert solution.stats.explored == 8
    assert solution.state.best == graph[2, 2]


def test_3x3_cache() -> None:
    """
    ========================================================================
     Test BFS algorithm on a 3x3 grid graph with cache.
    ========================================================================
    """
    bfs = GenBFS.gen_3x3_cache()
    solution = bfs.run()
    graph = bfs._problem.graph
    path_true = [graph[0, 0], graph[0, 1], graph[0, 2],
                 graph[1, 2], graph[2, 2]]
    assert solution.path == path_true
    assert list(solution.state.generated) == [graph[1, 0]]
    assert solution.stats.generated == 3
    assert solution.state.explored == {graph[0, 0]}
    assert solution.stats.explored == 1
    assert solution.state.best == graph[0, 1]
