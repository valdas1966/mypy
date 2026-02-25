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


def test_distances_to_goal() -> None:
    """
    ========================================================================
     Test the distances_to_goal() method.
    ========================================================================
    """
    algo = AStarReusable.Factory.without_obstacles()
    algo.run()
    distances = algo.distances_to_goal()
    grid = algo.problem.grid
    expected = {grid[0][0]: 3, grid[0][1]: 2,
                grid[0][2]: 1, grid[0][3]: 0}
    received = {s.key: d for s, d in distances.items()}
    assert received == expected


def test_bounds_to_goal() -> None:
    """
    ========================================================================
     Test the bounds_to_goal() method (only non-path explored States).
    ========================================================================
    """
    algo = AStarReusable.Factory.with_obstacles()
    algo.run()
    bounds = algo.bounds_to_goal()
    grid = algo.problem.grid
    # (1,0) is the only explored state not on the optimal path
    # g(1,0)=1, g_goal=7, bound=6
    expected = {grid[1][0]: 6}
    received = {s.key: b for s, b in bounds.items()}
    assert received == expected


def test_propagate_bounds() -> None:
    """
    ========================================================================
     Test the propagate_bounds() method with depth=2.
     On this grid, propagated bounds are <= h-values for all neighbors,
      so only the original bound for (1,0) survives the pruning.
    ========================================================================
    """
    algo = AStarReusable.Factory.with_obstacles()
    algo.run()
    bounds = algo.propagate_bounds(depth=2)
    grid = algo.problem.grid
    # (1,0) bound=6, h=4 → kept (6 > 4)
    # (2,0) from (1,0): bound=5, h=5 → pruned (5 <= 5)
    # (3,1) from (2,1): bound=3, h=5 → pruned (3 <= 5)
    # (3,2) from (2,2): bound=2, h=4 → pruned (2 <= 4)
    # (3,3) from (2,3): bound=1, h=3 → pruned (1 <= 3)
    expected = {grid[1][0]: 6}
    received = {s.key: b for s, b in bounds.items()}
    assert received == expected
