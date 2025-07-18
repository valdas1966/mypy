import pytest
from f_ds.old_grids.old_grid import Grid
from f_ds.old_grids.generators.g_grid import GenGrid
from f_file_old.generators.g_map_grid import GenMapGrid


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


def test_cells_valid(ex):
    assert ex.cells_valid.to_list() == [ex[0][0], ex[0][1], ex[0][2],
                                        ex[1][0], ex[1][1], ex[1][2]]
    assert len(ex.cells_valid) == 6
    assert ex.cells_valid.pct() == 100
    [cell.set_invalid() for cell in (ex[0][0], ex[0][1], ex[0][2])]
    assert len(ex.cells_valid) == 3
    assert ex.cells_valid.pct() == 50


def test_random() -> None:
    """
    ============================================================================
     Test the random method.
    ============================================================================
    """
    grid = GenGrid.random(rows=10, pct_invalid=20)
    assert len(grid) == 100
    assert len(grid.cells_valid) == 80


def test_distance_avg():
    """
    ============================================================================
     Test the distance_avg() method.
    ============================================================================
    """
    grid = GenGrid.full_3x3()    
    cells = [grid[0][0], grid[0][2], grid[2][0]]
    assert grid.distance_avg(cells) == 3


def test_from_array() -> None:
    """
    ============================================================================
     Test the from_array method.
    ============================================================================
    """
    grid = GenGrid.random(rows=10, pct_invalid=20)
    array = grid.to_array()
    grid_from_array = Grid.from_array(array=array)
    assert grid == grid_from_array


def test_from_map_grid() -> None:
    """
    ============================================================================
     Test the from_map_grid method.
    ============================================================================
    """
    path = 'd:\\temp\\map_grid.txt'
    GenMapGrid.map_grid(path=path)
    grid = Grid.from_map_grid(path=path)
    assert grid.name == 'map_grid'
    assert grid.rows == 3
    assert grid.cols == 3
    assert len(grid.cells_valid) == 8


def test_offsets_cell_col():
    """
    ============================================================================
     Test the offsets_cell_col() method.
    ============================================================================
    """
    grid = Grid.generate(rows=10)
    cell = grid[1][2]
    offsets = grid._offsets_cell_col(cell=cell, dist=20)
    assert offsets == (-2, 7)


def test_offsets_cell_row():
    """
    ============================================================================
     Test the offsets_cell_row() method.
    ============================================================================
    """
    grid = Grid.generate(rows=10)
    cell = grid[1][2]
    offsets = grid._offsets_cell_row(cell=cell, dist=20)
    assert offsets == (-1, 8)


def test_cells_within_distance():
    """
    ============================================================================
     Test the cells_within_distance() method.
    ============================================================================
    """ 
    grid = Grid.generate(rows=10)
    cell = grid[0][0]
    cells_within = grid.cells_within_distance(cell=cell, dist_max=2)
    assert len(cells_within) == 5
