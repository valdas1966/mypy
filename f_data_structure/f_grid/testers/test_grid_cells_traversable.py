from f_data_structure.f_grid.grid_cells_traversable import GridCellsTraversable


def test_cells_traversable():
    grid = GridCellsTraversable(2)
    assert len(grid.cells_traversable()) == 4
    grid[0][0].is_traversable = False
    assert len(grid.cells_traversable()) == 3


def test_num_cells_traversable():
    grid = GridCellsTraversable(2)
    grid[1][1].is_traversable = False
    assert grid.num_cells_traversable() == 3


def test_num_cells_non_traversable():
    grid = GridCellsTraversable(2)
    grid[1][1].is_traversable = False
    assert grid.num_cells_non_traversable() == 1


def test_pct_cells_traversable():
    grid = GridCellsTraversable(2)
    grid[1][1].is_traversable = False
    assert grid.pct_cells_traversable() == 0.75


def test_pct_cells_not_traversable():
    grid = GridCellsTraversable(2)
    grid[1][1].is_traversable = False
    assert grid.pct_cells_non_traversable() == 0.25


def test_generate():
    grid = GridCellsTraversable.generate(num_rows=5, pct_non_traversable=40)
    assert grid.num_cells_not_traversable() == 10
