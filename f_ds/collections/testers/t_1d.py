import pytest
from f_ds.collections.i_1d import Collection1D
from f_utils import u_int


@pytest.fixture
def ex_empty() -> Collection1D:
    return Collection1D()

@pytest.fixture
def ex_full() -> Collection1D:
    return Collection1D(name='Test', items=[1, 2])


def test_init(ex_empty, ex_full):
    assert ex_empty.name is None
    assert ex_full.name == 'Test'

def test_to_list(ex_full):
    assert ex_full.to_list() == [1, 2]

def test_contains(ex_empty, ex_full):
    assert 2 not in ex_empty
    assert 2 in ex_full


def test_len(ex_empty, ex_full):
    assert len(ex_empty) == 0
    assert len(ex_full) == 2


def test_bool(ex_empty, ex_full):
    assert not ex_empty
    assert ex_full


def test_str(ex_empty, ex_full):
    assert str(ex_empty) == 'None([])'
    assert str(ex_full) == 'Test([1, 2])'


def test_repr(ex_empty, ex_full):
    assert repr(ex_empty) == '<Collection1D: None([])>'
    assert repr(ex_full) == '<Collection1D: Test([1, 2])>'


def test_iter(ex_empty, ex_full):
    assert [x for x in ex_empty] == []
    assert [x for x in ex_full] == [1, 2]
