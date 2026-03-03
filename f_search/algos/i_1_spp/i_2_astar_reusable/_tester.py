from f_search.algos.i_1_spp.i_2_astar_reusable import AStarReusable


def test_with_data() -> None:
    """
    ========================================================================
     Test AStarReusable with pre-existing Data.
    ========================================================================
    """
    algo = AStarReusable.Factory.without_obstacles_with_cell_00()
    algo.run()
    assert algo._output.stats.explored == 2
    assert algo._output.stats.discovered == 4
