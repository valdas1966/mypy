from f_search.algos.i_1_spp.utils import (Grid, are_reachable,
                                          cells_reachable)


def test_are_reachable() -> None:
    """
    ========================================================================
     Test the are_reachable() function.
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


def test_cells_reachable() -> None:
    """
    ========================================================================
     Test the cells_reachable() function.
    ========================================================================
    """
    grid = Grid.Factory.four_without_obstacles()
    start = grid[0][0]
    received = cells_reachable(grid=grid, cell=start, steps_max=2)
    expected = [grid[0][0], grid[0][1], grid[0][2],
                grid[1][0], grid[1][1], grid[2][0]]
    assert received == expected
