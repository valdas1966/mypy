from f_ds.graphs.i_1_grid import GraphGrid, Grid, NodeCell


def test_neighbors():
    grid = Grid(rows=3)
    node = NodeCell(cell=grid[0][0])
    graph = GraphGrid(grid=grid)
    assert graph.neighbors(node=node) == [graph[0, 1], graph[1, 0]]
