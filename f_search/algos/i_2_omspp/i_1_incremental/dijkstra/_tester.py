from f_search.algos.i_2_omspp.i_1_incremental.dijkstra import DijkstraIncremental


def test_dijkstra_incremental():
    """
    ========================================================================
     Test the Dijkstra Algorithm for One-to-Many Shortest-Path-Problem.
    ========================================================================
    """
    algo = DijkstraIncremental.Factory.without_obstacles()
    solution = algo.run()
    stats = solution.stats
    assert stats.explored == 15
    assert stats.generated == 16
