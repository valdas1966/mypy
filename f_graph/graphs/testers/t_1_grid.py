import pytest
from f_graph.graphs.i_1_grid import GraphGrid, Grid, NodePathCell


@pytest.fixture
def ex() -> GraphGrid:
    grid = Grid(rows=3)
    grid[1][1].set_invalid()
    return GraphGrid(grid=grid)


def test_getitem(ex):
    node = ex[1, 2]
    assert node.cell.row, node.cell.col == (1, 2)


def test_neighbors(ex):
    node = NodePathCell(cell=ex.grid[0][0])
    assert ex.neighbors(node=node) == [ex[0, 1], ex[1, 0]]


def test_len(ex):
    assert len(ex) == 8
