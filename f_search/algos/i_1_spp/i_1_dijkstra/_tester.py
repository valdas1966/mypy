from f_search.algos.i_1_spp.i_1_dijkstra.main import Dijkstra


def test_dijkstra() -> None:
    """
    ========================================================================
     Test Dijkstra's Algorithm.
    ========================================================================
    """
    algo = Dijkstra.Factory.without_obstacles()
    solution = algo.run()
    cells_path = [state.key for state in solution.path._states]
    grid = algo.problem.grid
    cells_true = [grid[0][0], grid[0][1], grid[0][2], grid[0][3]]
    assert cells_path == cells_true
    cells_explored = {state.key for state in algo._data.explored}
    assert cells_explored == {grid[0][0], grid[0][1], grid[0][2],
                              grid[1][0], grid[1][1], grid[2][0]}
    cells_generated_true = {grid[1][2], grid[2][1], grid[3][0]}
    cells_generated = {state.key for state in algo._data.frontier}
    assert cells_generated == cells_generated_true
    assert solution.stats.explored == 6
    assert solution.stats.discovered == 10
