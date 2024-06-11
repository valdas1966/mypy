import pytest
from f_ds.grids.grid import Grid


@pytest.fixture
def ex() -> Grid:
    return Grid(2, 3)


def test_getitem(ex):
    row = 1
    col = 2
    cell = ex[row][col]
    assert (cell.row, cell.col) == (row, col)

def test_distance(ex):
    cell_0 = ex[0][0]
    cell_1 = ex[1][1]
    assert ex.distance(cell_0, cell_0) == 0
    assert ex.distance(cell_0, cell_1) == 2

def test_neighbors(ex):
    cell_00 = ex[0][0]
    cell_01 = ex[0][1]
    cell_10 = ex[1][0]
    assert ex.neighbors(cell_00) == [cell_01, cell_10]