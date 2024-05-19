from f_ds.grids.cell import Cell


def test_distance():
    cell_1 = Cell(1, 2)
    cell_2 = Cell(3, 2)
    assert cell_1.distance(cell_1) == 0
    assert cell_1.distance(cell_2) == 2
