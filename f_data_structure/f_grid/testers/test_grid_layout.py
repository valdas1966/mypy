from f_data_structure.f_grid.grid_layout import GridLayout
from f_data_structure.f_grid.row_col import RowCol
from f_data_structure.f_grid.cell import Cell


def test_shape():
    grid = GridLayout(2)
    assert grid.shape() == '(2,2)'


def test_name():
    grid = GridLayout(2, name='Test')
    assert grid.name == 'Test(2,2)'


def test_is_within():
    grid = GridLayout(5)
    assert grid.is_within(RowCol(2, 3))
    assert not grid.is_within(RowCol(-1, 0))
    assert not grid.is_within(RowCol(10, 5))
    assert grid.is_within(Cell(2, 3))


def test_filter_valid():
    grid = GridLayout(5)
    cell = Cell(4, 4)
    neighbors = cell.neighbors()
    assert grid.filter_valid(neighbors) == [Cell(3, 4), Cell(4, 3)]
