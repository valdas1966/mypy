from f_search.algos.i_1_neighborhood.main import BFSNeighborhood


def test_name_algo() -> None:
    """
    ========================================================================
     Test that solution.name_algo matches the Algorithm's Name.
    ========================================================================
    """
    bfs = BFSNeighborhood.Factory.without_obstacles()
    solution = bfs.run()
    assert solution.name_algo == 'BFSNeighborhood'


def test_without_obstacles() -> None:
    """
    ========================================================================
     Test the BFSNeighborhood algorithm without obstacles.
    ========================================================================
    """
    bfs = BFSNeighborhood.Factory.without_obstacles()
    grid = bfs.problem.grid
    solution = bfs.run()
    neighborhood = {state.key for state in solution.neighborhood}
    assert neighborhood == {grid[0][0], grid[0][1], grid[1][0]}
