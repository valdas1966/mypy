from f_search.algos.i_1_spp.i_2_dijkstra import Dijkstra


def test_without_obstacles() -> None:
    """
    ========================================================================
     Test Dijkstra algorithm without obstacles.
    ========================================================================
    """
    dijkstra = Dijkstra.Factory.without_obstacles()
    solution = dijkstra.run()
    cells_path = [state.key for state in solution.path._states]
    grid = dijkstra._problem.grid
    cells_path_true = [grid[0][0], grid[0][1], grid[0][2], grid[0][3]]
    assert cells_path == cells_path_true
    cells_explored = {state.key for state in dijkstra._data.explored}
    cells_explored_true = {grid[0][0], grid[0][1], grid[1][0], grid[0][2],
                           grid[1][1], grid[2][0]}
    assert cells_explored == cells_explored_true
    cells_generated = [state.key for state in dijkstra._data.generated]
    cells_generated_true = [grid[1][2], grid[2][1], grid[3][0]]
    assert cells_generated == cells_generated_true


def test_with_obstacles() -> None:
    """
    ========================================================================
     Test Dijkstra algorithm with obstacles.
    ========================================================================
    """
    dijkstra = Dijkstra.Factory.with_obstacles()
    solution = dijkstra.run()
    cells_path = [state.key for state in solution.path._states]
    grid = dijkstra._problem.grid
    cells_true = [grid[0][0], grid[0][1], grid[1][1], grid[2][1],
                  grid[2][2], grid[2][3], grid[1][3], grid[0][3]]
    assert cells_path == cells_true
    cells_explored = {state.key for state in dijkstra._data.explored}
    cells_explored_true = {grid[0][0], grid[0][1],
                           grid[1][0], grid[1][1], grid[1][3],
                           grid[2][0], grid[2][1], grid[2][2], grid[2][3],
                           grid[3][0], grid[3][1], grid[3][2], grid[3][3]}
    assert cells_explored == cells_explored_true
    cells_generated = {state.key for state in dijkstra._data.generated}
    cells_generated_true = set()
    assert cells_generated == cells_generated_true


def test_counters_without_obstacles() -> None:
    """
    ========================================================================
     Test that generated and explored counters match actual list/set sizes.
    ========================================================================
    """
    dijkstra = Dijkstra.Factory.without_obstacles()
    solution = dijkstra.run()
    assert solution.stats.generated == 10
    assert solution.stats.explored == 6


def test_counters_with_obstacles() -> None:
    """
    ========================================================================
     Test that generated and explored counters match actual list/set sizes.
    ========================================================================
    """
    dijkstra = Dijkstra.Factory.with_obstacles()
    solution = dijkstra.run()
    assert solution.stats.generated == 14
    assert solution.stats.explored == 13
