from f_hs.algo.i_2_dijkstra import Dijkstra


def test_grid_3x3_path_found() -> None:
    """
    ========================================================================
     Test Dijkstra on open 3x3 grid finds optimal path (cost 4).
    ========================================================================
    """
    algo = Dijkstra.Factory.grid_3x3()
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
     Test Dijkstra on 3x3 grid with an obstacle still finds a path.
    ========================================================================
    """
    algo = Dijkstra.Factory.grid_3x3_obstacle()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 4.0


def test_grid_3x3_no_path() -> None:
    """
    ========================================================================
     Test Dijkstra on 3x3 grid with a wall returns invalid.
    ========================================================================
    """
    algo = Dijkstra.Factory.grid_3x3_no_path()
    solution = algo.run()
    assert bool(solution) is False
    assert solution.cost == float('inf')


def test_grid_3x3_start_is_goal() -> None:
    """
    ========================================================================
     Test Dijkstra on grid where start == goal (cost 0, path length 1).
    ========================================================================
    """
    algo = Dijkstra.Factory.grid_3x3_start_is_goal()
    solution = algo.run()
    assert bool(solution) is True
    assert solution.cost == 0.0
    path = algo.reconstruct_path()
    assert len(path) == 1
