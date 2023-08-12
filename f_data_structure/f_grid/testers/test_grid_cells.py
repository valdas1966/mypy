from f_data_structure.f_grid.grid_cells import GridCells


def test_cells():
    grid = GridCells(2)
    cells = grid.cells()
    assert len(cells) == 4


def test_get():
    grid = GridCells(2, 3)
    grid[1][2].name = 'A'
    cell = grid.cells()[-1]
    assert cell.row == 1
    assert cell.col == 2
    assert cell.name == 'A'


def test_cells_random():
    grid = GridCells(5)
    assert len(grid.cells_random(size=15)) == 15
    assert len(grid.cells_random(pct=40)) == 10
