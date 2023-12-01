from f_data_structure.f_grid.grid_cells import GridCells
from f_data_structure.f_grid.cell import Cell


def test_init():
    grid = GridCells(2)
    assert grid[0][0] == Cell(0, 0)
    assert grid[0][1] == Cell(0, 1)
    assert grid[1][0] == Cell(1, 0)
    assert grid[1][1] == Cell(1, 1)


def test_cells():
    grid = GridCells(2)
    cells = grid.cells()
    assert cells == [Cell(0, 0), Cell(0, 1), Cell(1, 0), Cell(1, 1)]


def test_get():
    grid = GridCells(2, 3)
    grid[1][2].name = 'A'
    cell = grid.cells()[-1]
    assert cell == Cell(1, 2)
    assert cell.name == 'A'


def test_cells_random():
    grid = GridCells(5)
    assert len(grid.cells_random(size=15)) == 15
    assert len(grid.cells_random(pct=40)) == 10


def test_neighbors():
    grid = GridCells(5)
    cell = grid[0][0]
    assert grid.neighbors(cell) == [Cell(0, 1), Cell(1, 0)]


def test_make_invalid():
    grid = GridCells(2)
    row = grid[0]
    grid.make_invalid(cells=row)
    assert not grid[0][0].is_valid and not grid[0][1].is_valid
    grid.make_invalid(cells=[(1, 0), (1, 1)])
    assert not grid[1][0].is_valid and not grid[1][1].is_valid


def test_pct_cells_valid():
    grid = GridCells.generate(rows=5, pct_non_valid=40)
    assert grid.pct_cells_valid() == 0.6
