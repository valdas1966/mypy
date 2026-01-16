from f_search.algos.i_1_spp.i_3_dijkstra_neighborhood import DijkstraNeighborhood as Algo
from f_ds.grids import GridMap as Grid


def test_with_obstacles() -> None:
    """
    ===========================================================================
     Test creating K-Neighborhood by Dijkstra algorithm.
    ===========================================================================
    """
    grid = Grid.Factory.four_with_obstacles()
    dijkstra = Algo.Factory.grid_4x4_with_obstacles()
    neighborhood = dijkstra.run()
    neighborhood_true = {grid[0][0], grid[0][1],
                         grid[1][0], grid[1][1],
                         grid[2][0]}
    assert neighborhood == neighborhood_true


def test_without_obstacles() -> None:
    """
    ===========================================================================
     Test creating K-Neighborhood by Dijkstra algorithm.
    ===========================================================================
    """
    grid = Grid.Factory.four_without_obstacles()
    dijkstra = Algo.Factory.grid_4x4_without_obstacles()
    neighborhood = dijkstra.run()
    neighborhood_true = {grid[0][0], grid[0][1],
                         grid[1][0], grid[1][1],
                         grid[0][2], grid[2][0]}
    assert neighborhood == neighborhood_true
