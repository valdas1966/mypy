from f_data_structure.f_grid.cell import Cell


def test_str():
    cell = Cell(1, 2)
    assert str(cell) == '(1,2)'
    cell = Cell(3)
    assert str(cell) == '(3,3)'


def test_eq():
    cell_1 = Cell(1)
    cell_2 = Cell(2)
    cell_3 = Cell(1)
    assert cell_1 == cell_3
    assert not cell_1 == cell_2


def test_distance():
    cell_1 = Cell(1, 2)
    cell_2 = Cell(3, 2)
    assert cell_1.distance(cell_1) == 0
    assert cell_1.distance(cell_2) == 2


def test_comparison():
    assert Cell(0, 0) < Cell(0, 1) <= Cell(1, 0) <= Cell(1, 1)
