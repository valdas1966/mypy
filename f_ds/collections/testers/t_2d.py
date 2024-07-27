import pytest
from f_ds.collections.old.old_i_2d import Collection2D


@pytest.fixture
def ex() -> Collection2D:
    items = [[1, 2], [3, 4]]
    return Collection2D(items=items)


def test_to_list(ex):
    assert ex.to_list() == [1, 2, 3, 4]


def test_str(ex):
    assert str(ex) == 'None(2,2)'
