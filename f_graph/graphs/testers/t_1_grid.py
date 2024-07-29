import pytest
from f_graph.graphs.i_1_grid import GraphGrid, Grid, NodeCell


@pytest.fixture
def ex() -> GraphGrid:
    grid = Grid(rows=3)
    return GraphGrid(grid=grid)


def test_getitem(ex):
    node = ex[1, 2]
    assert node.cell.row, node.cell.col == (1, 2)


def test_neighbors(ex):
    node = NodeCell(cell=ex.grid[0][0])
    assert ex.neighbors(node=node) == [ex[0, 1], ex[1, 0]]
