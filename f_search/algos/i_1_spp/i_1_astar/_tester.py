from f_search.algos.i_1_spp.i_1_astar import AStar


def test_without_obstacles() -> None:
    """
    ========================================================================
     Test AStar algorithm without obstacles.
    ========================================================================
    """
    astar = AStar.Factory.without_obstacles()
    solution = astar.run()
    path = astar._data.path_to(state=astar.problem.goal)
    cells_path = [state.key for state in path._states]
    grid = astar.problem.grid
    cells_true = [grid[0][0], grid[0][1], grid[0][2], grid[0][3]]
    assert cells_path == cells_true
    cells_explored = {state.key for state in astar._data.explored}
    assert cells_explored == set(cells_true[:-1])
    cells_generated_true = [grid[1][0], grid[1][1], grid[1][2]]
    cells_generated = [state.key for state in astar._data.frontier]
    assert cells_generated == cells_generated_true
    assert solution.stats.discovered == 7
    assert solution.stats.explored == 3

def test_with_obstacles() -> None:
    """
    ========================================================================
     Test AStar algorithm without obstacles.
    ========================================================================
    """
    astar = AStar.Factory.with_obstacles()
    solution = astar.run()
    path = astar._data.path_to(state=astar.problem.goal)
    cells_path = [state.key for state in path._states]
    grid = astar.problem.grid
    cells_true = [grid[0][0], grid[0][1], grid[1][1], grid[2][1],
                  grid[2][2], grid[2][3], grid[1][3], grid[0][3]]
    assert cells_path == cells_true
    cells_explored = {state.key for state in astar._data.explored}
    assert cells_explored == set(cells_true[:-1]) | {grid[1][0]}
    cells_generated_true = [grid[2][0], grid[3][1], grid[3][2], grid[3][3]]
    cells_generated = [state.key for state in astar._data.frontier]
    assert cells_generated == cells_generated_true
    assert solution.stats.discovered == 13
    assert solution.stats.explored == 8


def test_quality_h_without_obstacles() -> None:
    """
    ========================================================================
     Test the quality_h property without obstacles.
    ========================================================================
    """
    astar = AStar.Factory.without_obstacles()
    solution = astar.run()
    assert solution.quality_h == 1.0


def test_quality_h_with_obstacles() -> None:
    """
    ========================================================================
     Test the quality_h property with obstacles.
    ========================================================================
    """
    astar = AStar.Factory.with_obstacles()
    solution = astar.run()
    assert solution.quality_h == 3 / 7


def test_efficiency_without_obstacles() -> None:
    """
    ========================================================================
     Test the efficiency property without obstacles.
    ========================================================================
    """
    astar = AStar.Factory.without_obstacles()
    solution = astar.run()
    assert solution.efficiency == 4 / 3


def test_efficiency_with_obstacles() -> None:
    """
    ========================================================================
     Test the efficiency property with obstacles.
    ========================================================================
    """
    astar = AStar.Factory.with_obstacles()
    solution = astar.run()
    assert solution.efficiency == 8 / 8


def test_closed_categories_without_obstacles() -> None:
    """
    ========================================================================
     Test closed_categories() without obstacles (perfect heuristic).
    ========================================================================
    """
    astar = AStar.Factory.without_obstacles()
    astar.run()
    categories = astar.closed_categories()
    grid = astar.problem.grid
    surely = {s.key for s in categories['Surely Expanded']}
    borderline = {s.key for s in categories['Borderline']}
    assert surely == set()
    assert borderline == {grid[0][0], grid[0][1], grid[0][2]}


def test_closed_categories_with_obstacles() -> None:
    """
    ========================================================================
     Test closed_categories() with obstacles.
    ========================================================================
    """
    astar = AStar.Factory.with_obstacles()
    astar.run()
    categories = astar.closed_categories()
    grid = astar.problem.grid
    surely = {s.key for s in categories['Surely Expanded']}
    borderline = {s.key for s in categories['Borderline']}
    assert surely == {grid[0][0], grid[0][1],
                      grid[1][0], grid[1][1]}
    assert borderline == {grid[2][1], grid[2][2],
                          grid[2][3], grid[1][3]}
