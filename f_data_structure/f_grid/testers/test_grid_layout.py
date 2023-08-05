from f_data_structure.f_grid.grid_layout import GridLayout
from f_data_structure.f_grid.location_row_col import LocationRowCol


def test_shape():
    grid = GridLayout(2)
    assert grid.shape() == '(2,2)'

    
def test_is_within():
    grid = GridLayout(5)
    loc = LocationRowCol(2, 3)
    assert grid.is_within(1, 2)
    assert grid.is_within(loc=loc)
    assert not grid.is_within(-1, 0)
    assert not grid.is_within(10, 2)
