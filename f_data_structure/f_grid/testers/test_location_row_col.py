from f_data_structure.f_grid.location_row_col import LocationRowCol


def test_distance():
    loc_1 = LocationRowCol(1, 2)
    loc_2 = LocationRowCol(3, 4)
    assert loc_1.distance(loc_1) == 0
    assert loc_1.distance(loc_2) == 4


def test_order():
    loc_1 = LocationRowCol(1)
    loc_2 = LocationRowCol(1, 2)
    loc_3 = LocationRowCol(2, 1)
    assert loc_1 == loc_1
    assert loc_1 < loc_2
    assert loc_3 >= loc_2
