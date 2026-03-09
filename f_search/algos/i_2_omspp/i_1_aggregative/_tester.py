from f_search.algos.i_2_omspp.i_1_aggregative import AStarAggregative


def test_aggregative() -> None:
    """
    ========================================================================
     Test the A* Aggregative Algorithm.
    ========================================================================
    """
    algo = AStarAggregative.Factory.without_obstacles()
    solution = algo.run()
    stats = solution.stats
    assert stats.explored == 6
    assert stats.discovered == 11


def test_quality_h() -> None:
    """
    ========================================================================
     Test quality_h without obstacles (perfect heuristic).
    ========================================================================
    """
    algo = AStarAggregative.Factory.without_obstacles()
    solution = algo.run()
    assert solution.quality_h == 1.0
