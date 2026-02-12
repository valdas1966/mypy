from f_search.algos.i_2_omspp.i_1_incremental.bfs import BFSIncremental


def test_without_obstacles() -> None:
    """
    ========================================================================
     Test the Incremental BFS Algorithm for OMSPP without obstacles.
    ========================================================================
    """
    bfs = BFSIncremental.Factory.without_obstacles()
    solution = bfs.run()
    assert solution.stats.explored == 15
    assert solution.stats.discovered == 16
    assert solution.subs[0].stats.explored == 6
    assert solution.subs[0].stats.discovered == 10
    assert solution.subs[1].stats.explored == 9
    assert solution.subs[1].stats.discovered == 6
