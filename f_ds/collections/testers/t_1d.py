import pytest
from f_ds.collections.i_1d import Collection1D
from f_utils import u_int


@pytest.fixture
def ex_empty() -> Collection1D:
    return Collection1D(items=list())

@pytest.fixture
def ex_full() -> Collection1D:
    return Collection1D(name='Test', items=[1, 2])


def test_init(ex_empty, ex_full):
    assert ex_empty.name is None
    assert ex_full.name == 'Test'


def test_str(ex_empty, ex_full):
    assert str(ex_empty) == 'None([])'
    assert str(ex_full) == 'Test([1, 2])'
