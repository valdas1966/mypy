from f_search.algos import KDijkstra


def test_without_obstacles():
    """
    ========================================================================
     Test the KDijkstra algorithm without obstacles.
    ========================================================================
    """
    algo = KDijkstra.Factory.without_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 15
    assert solution.stats.generated == 16
    grid = algo._problem.grid
    goal_1, goal_2 = algo._problem.goals
    cells_path_1 = [state.key for state in solution.paths[goal_1]._states]
    cells_path_1_true = [grid[0][0], grid[0][1], grid[0][2], grid[0][3]]
    assert cells_path_1 == cells_path_1_true
    cells_path_2 = [state.key for state in solution.paths[goal_2]._states]
    cells_path_2_true = [grid[0][0], grid[0][1], grid[0][2], grid[0][3],
                         grid[1][3], grid[2][3], grid[3][3]]
    assert cells_path_2 == cells_path_2_true


def test_with_obstacles():
    """
    ========================================================================
     Test the KDijkstra algorithm with obstacles.
    ========================================================================
    """
    algo = KDijkstra.Factory.with_obstacles()
    solution = algo.run()
    assert solution.stats.explored == 13
    assert solution.stats.generated == 14
    grid = algo._problem.grid
    goal_1, goal_2 = algo._problem.goals
    cells_path_1 = [state.key for state in solution.paths[goal_1]._states]
    cells_path_1_true = [grid[0][0], grid[0][1], grid[1][1], grid[2][1],
                         grid[2][2], grid[2][3], grid[1][3], grid[0][3]]
    assert cells_path_1 == cells_path_1_true
    cells_path_2 = [state.key for state in solution.paths[goal_2]._states]
    cells_path_2_true = [grid[0][0], grid[0][1], grid[1][1], grid[2][1],
                         grid[2][2], grid[2][3], grid[3][3]]
    assert cells_path_2 == cells_path_2_true
