from f_search.algos.i_2_omspp.i_1_kx_astar import KxAStar


def test_without_obstacles():
    """
    ========================================================================
     Test the KxAStar algorithm without obstacles.
    ========================================================================
    """
    algo = KxAStar.Factory.without_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 3 + 6
    assert solution.stats.generated == 7 + 11
    

def test_with_obstacles():
    """
    ========================================================================
     Test the KxAStar algorithm with obstacles.
    ========================================================================
    """
    algo = KxAStar.Factory.with_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 8 + 6
    assert solution.stats.generated == 13 + 12
