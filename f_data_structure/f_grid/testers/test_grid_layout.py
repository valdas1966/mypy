from f_data_structure.f_grid.grid_layout import GridLayout


def test_shape():
    grid = GridLayout(2)
    assert grid.shape() == '(2,2)'


def test_name():
    grid = GridLayout(2, name='Test')
    assert grid.name == 'Test(2,2)'


def test_is_within():
    grid = GridLayout(5)
    assert grid.is_within(2, 3)
    assert not grid.is_within(-1, 0)
    assert not grid.is_within(10, 5)
    assert grid.is_within(2, 3)
