from f_data_structure.f_grid.cell import Cell


def test_neighbors():
    cell = Cell(1, 2)
    north = Cell(2, 2)
    east = Cell(1, 3)
    south = Cell(0, 2)
    west = Cell(1, 1)
    expected = [north, east, south, west]
    assert cell.neighbors() == expected
