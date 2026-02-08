from f_search.algos.i_2_omspp.i_1_repeated.astar import AStarRepeated


def test_without_obstacles():
    """
    ========================================================================
     Test the KxAStar algorithm without obstacles.
    ========================================================================
    """
    algo = AStarRepeated.Factory.without_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 3 + 6
    assert solution.stats.discovered == 7 + 11
    

def test_with_obstacles():
    """
    ========================================================================
     Test the KxAStar algorithm with obstacles.
    ========================================================================
    """
    algo = AStarRepeated.Factory.with_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 8 + 6
    assert solution.stats.discovered == 13 + 12
