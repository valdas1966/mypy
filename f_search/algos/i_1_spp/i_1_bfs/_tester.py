from f_search.algos.i_1_spp.i_1_bfs import BFS


def test_without_obstacles() -> None:
    """
    ========================================================================
     Test BFS algorithm without obstacles.
    ========================================================================
    """
    bfs = BFS.Factory.without_obstacles()
    solution = bfs.run()
    cells_path = [state.key for state in solution.path._states]
    grid = bfs.problem.grid
    cells_true = [grid[0][0], grid[0][1], grid[0][2], grid[0][3]]
    assert cells_path == cells_true
    cells_explored = {state.key for state in bfs._data.explored}
    assert cells_explored == {grid[0][0], grid[0][1], grid[0][2],
                              grid[1][0], grid[1][1], grid[2][0]}
    cells_generated_true = {grid[1][2], grid[2][1], grid[3][0]}
    cells_generated = {state.key for state in bfs._data.frontier}
    assert cells_generated == cells_generated_true


def test_without_obstacles_with_cell_00() -> None:
    """
    ========================================================================
     Test BFS algorithm without obstacles with an explored Cell(0,0).
    ========================================================================
    """
    bfs = BFS.Factory.without_obstacles_with_cell_00()
    solution = bfs.run()
    cells_path = [state.key for state in solution.path._states]
    grid = bfs.problem.grid
    cells_true = [grid[0][0], grid[0][1], grid[0][2], grid[0][3]]
    assert cells_path == cells_true
    cells_explored = {state.key for state in bfs._data.explored}
    assert cells_explored == {grid[0][0], grid[0][1], grid[0][2],
                              grid[1][0], grid[1][1], grid[2][0]}
    cells_generated_true = {grid[1][2], grid[2][1], grid[3][0]}
    cells_generated = {state.key for state in bfs._data.frontier}
    assert cells_generated == cells_generated_true
    assert solution.stats.explored == 5
    assert solution.stats.discovered == 6

