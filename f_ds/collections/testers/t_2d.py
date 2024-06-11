import pytest
from f_ds.collections.i_2d import Collection2D


@pytest.fixture
def ex() -> Collection2D:
    items = [[1, 2], [3, 4]]
    return Collection2D(items=items)


def test_to_list(ex):
    assert ex.to_list() == [1, 2, 3, 4]

def test_contains(ex):
    assert 3 in ex


def test_len(ex):
    assert len(ex) == 4


def test_bool(ex):
    assert ex


def test_str(ex):
    assert str(ex) == 'None([1, 2, 3, 4])'


def test_repr(ex):
    assert repr(ex) == '<Collection2D: None([1, 2, 3, 4])>'


def test_iter(ex):
    assert [x for x in ex] == [1, 2, 3, 4]
