from f_search.algos.i_1_spp.i_3_dijkstra_neighborhood import DijkstraNeighborhood as Algo
from f_ds.grids import GridMap as Grid


def test_dijkstra_neighborhood() -> None:
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
