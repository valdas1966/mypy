from f_data_structure.f_grid.grid_cells_traversable import GridCellsTraversable
from f_data_structure.f_grid.cell_traversable import CellTraversable


def test_cells_traversable():
    grid = GridCellsTraversable(2)
    assert len(grid.cells()) == 4
    grid[0][0].is_traversable = False
    assert len(grid.cells()) == 3


def test_len():
    grid = GridCellsTraversable(2)
    assert len(grid) == 4
    grid[0][0].is_traversable = False
    assert len(grid) == 3


def test_pct_cells_traversable():
    grid = GridCellsTraversable(2)
    grid[1][1].is_traversable = False
    assert grid.pct_cells_traversable() == 0.75


def test_filter_valid():
    grid = GridCellsTraversable(5)
    grid[0][1].is_traversable = False
    cell = CellTraversable(0, 0)
    neighbors = cell.neighbors()
    assert grid.filter_valid(li=neighbors) == [CellTraversable(1, 0)]


def test_generate():
    grid = GridCellsTraversable.generate(rows=5, pct_non_traversable=40)
    assert len(grid) == 15
