import pytest
from f_ds.graphs.i_2_grid import GraphGrid, NodeCell, Grid


@pytest.fixture
def ex() -> GraphGrid:
    grid = Grid(rows=3)
    grid[1][1].set_invalid()
    return GraphGrid(grid=grid)


def test_getitem(ex):
    node = ex[1, 2]
    assert node.cell.row, node.cell.col == (1, 2)


def test_neighbors(ex):
    node = NodeCell(key=ex.grid[0][0])
    assert ex.neighbors(node=node) == [ex[0, 1], ex[1, 0]]


def test_len(ex):
    assert len(ex) == 8


def test_clone(ex):
    ex[0, 0].parent = ex[0, 1]
    cloned = ex.clone()
    assert ex[0, 0].parent == ex[0, 1]
    assert not cloned[0, 0].parent


def test_nodes_within_distance(ex):
    """
    ========================================================================
     Test the nodes_within_distance() method.
    ========================================================================
    """
    node = ex[0, 0]
    nodes_within_distance = ex.nodes_within_distance(node=node, dist_max=1)
    assert set(nodes_within_distance) == {ex[0, 1], ex[1, 0]}


def test_distance_avg(ex):
    """
    ========================================================================
     Test the distance_avg() method.
    ========================================================================
    """
    nodes = [ex[0, 0], ex[0, 2], ex[2, 0]]
    assert ex.distance_avg(nodes=nodes) == 3
