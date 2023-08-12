from f_data_structure.f_grid.row_col import RowCol


def test_distance():
    loc_1 = RowCol(1, 2)
    loc_2 = RowCol(3, 4)
    assert loc_1.distance(loc_1) == 0
    assert loc_1.distance(loc_2) == 4


def test_order():
    loc_1 = RowCol(1)
    loc_2 = RowCol(1, 2)
    loc_3 = RowCol(2, 1)
    assert loc_1 == loc_1
    assert loc_1 < loc_2
    assert loc_3 >= loc_2
