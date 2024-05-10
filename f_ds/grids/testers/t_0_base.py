from f_ds.grids.i_0_base import GridBase


def test_total():
    grid = GridBase(3)
    assert grid.total() == 9


def test_shape():
    grid = GridBase(2)
    assert grid.shape() == '(2,2)'


def test_name():
    grid = GridBase(2, name='Test')
    assert grid.name == 'Test(2,2)'


def test_is_within():
    grid = GridBase(5)
    assert grid.is_within(2, 3)
    assert not grid.is_within(-1, 0)
    assert not grid.is_within(10, 5)
    assert grid.is_within(2, 3)
