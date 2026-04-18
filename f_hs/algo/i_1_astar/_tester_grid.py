from f_hs.algo.i_1_astar import AStar


def test_grid_3x3_path_found() -> None:
    """
    ========================================================================
     Test AStar on open 3x3 grid finds optimal path (cost 4).
    ========================================================================
    """
    algo = AStar.Factory.grid_3x3()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 4.0
    path = algo.reconstruct_path()
    assert len(path) == 5
    assert path[0].key.row == 0 and path[0].key.col == 0
    assert path[-1].key.row == 2 and path[-1].key.col == 2


def test_grid_3x3_obstacle() -> None:
    """
    ========================================================================
     Test AStar on 3x3 grid with an obstacle still finds a path.
    ========================================================================
    """
    algo = AStar.Factory.grid_3x3_obstacle()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 4.0


def test_grid_3x3_no_path() -> None:
    """
    ========================================================================
     Test AStar on 3x3 grid with a wall returns invalid.
    ========================================================================
    """
    algo = AStar.Factory.grid_3x3_no_path()
    solution = algo.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_grid_3x3_start_is_goal() -> None:
    """
    ========================================================================
     Test AStar on grid where start == goal (cost 0, path length 1).
    ========================================================================
    """
    algo = AStar.Factory.grid_3x3_start_is_goal()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = algo.reconstruct_path()
    assert len(path) == 1
