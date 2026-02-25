from f_search.algos.i_2_omspp.i_1_aggregative import AStarAggregative


def test_name_algo() -> None:
    """
    ========================================================================
     Test that solution.name_algo matches the Algorithm's Name.
    ========================================================================
    """
    algo = AStarAggregative.Factory.without_obstacles()
    solution = algo.run()
    assert solution.name_algo == 'AStarAggregative'


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
