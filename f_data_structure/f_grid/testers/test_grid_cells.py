from f_data_structure.f_grid.grid_cells import GridCells


def test_cells():
    grid = GridCells(2)
    cells = grid.cells()
    assert len(cells) == 4


def test_get():
    grid = GridCells(2)
    grid[0][0].name == 'A'
    assert grid.cells()[0].name == 'A'
