import pytest
from f_graph.graphs.i_1_grid import GraphGrid, Grid, NodeCell


@pytest.fixture
def ex() -> GraphGrid:
    grid = Grid(rows=3)
    grid[1][1].set_invalid()
    return GraphGrid(grid=grid)


def test_getitem(ex):
    node = ex[1, 2]
    assert node.cell.row, node.cell.col == (1, 2)


def test_neighbors(ex):
    node = NodeCell(cell=ex.grid[0][0])
    assert ex.neighbors(node=node) == [ex[0, 1], ex[1, 0]]


def test_len(ex):
    assert len(ex) == 8


def test_copy(ex):
    ex[0, 0].parent = ex[0, 1]
    copied = ex.copy()
    assert ex[0, 0].parent == ex[0, 1]
    assert not copied[0, 0].parent
