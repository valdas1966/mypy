from f_search.algos.i_2_omspp.i_1_incremental.dijkstra.main import DijkstraIncremental


def test_dijkstra_incremental() -> None:
    """
    ========================================================================
     Test the Incremental Dijkstra's Algorithm for OMSPP.
    ========================================================================
    """
    algo = DijkstraIncremental.Factory.without_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 15
    assert solution.stats.discovered == 16
    assert solution.subs[0].stats.explored == 6
    assert solution.subs[0].stats.discovered == 10
    assert solution.subs[1].stats.explored == 9
    assert solution.subs[1].stats.discovered == 6
