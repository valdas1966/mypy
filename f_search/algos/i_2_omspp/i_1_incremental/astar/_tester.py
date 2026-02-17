from f_search.algos.i_2_omspp.i_1_incremental.astar import AStarIncremental


def test_astar_incremental():
    """
    ========================================================================
     Test the A* Algorithm for One-to-Many Shortest-Path-Problem.
    ========================================================================
    """
    algo = AStarIncremental.Factory.without_obstacles()
    solution = algo.run()
    stats = solution.stats
    assert stats.explored == 6
    assert stats.discovered == 11
