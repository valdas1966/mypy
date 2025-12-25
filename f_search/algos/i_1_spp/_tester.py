from f_search.algos.i_1_spp.utils import are_reachable, Grid


def test_are_reachable() -> None:
    """
    ========================================================================
     Test the are_reachable function.
    ========================================================================
    """
    grid_reachable = Grid.Factory.four_with_obstacles()
    start = grid_reachable[0][0]
    goal = grid_reachable[0][3]
    assert are_reachable(grid_reachable, start, goal)
    grid_unreachable = Grid.Factory.x()
    start = grid_unreachable[0][1]
    goal = grid_unreachable[1][0]
    assert not are_reachable(grid_unreachable, start, goal)
