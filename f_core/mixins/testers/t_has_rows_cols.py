import pytest
from f_core.mixins.has_rows_cols import HasRowsCols


@pytest.fixture
def ex_11() -> HasRowsCols:
    return HasRowsCols(1)

@pytest.fixture
def ex_23() -> HasRowsCols:
    return HasRowsCols(rows=2, cols=3)

@pytest.fixture
def ex_32() -> HasRowsCols:
    return  HasRowsCols(3, 2)


def test_init(ex_11, ex_23):
    assert ex_11.rows, ex_11.cols == (1, 1)
    assert ex_23.rows, ex_23.cols == (2, 3)

def test_shape(ex_11, ex_23):
    assert ex_11.shape() == '(1,1)'
    assert ex_23.shape() == '(2,3)'

def test_is_within(ex_11, ex_23):
    assert not ex_11.is_within(row=1, col=1)
    assert ex_23.is_within(row=1, col=1)

def test_key_comparison(ex_11, ex_23, ex_32):
    assert ex_11 < ex_23 < ex_32

def test_len(ex_11, ex_23):
    assert len(ex_11) == 1
    assert len(ex_23) == 6

def test_str(ex_11):
    assert str(ex_11) == '(1,1)'

def test_hash(ex_23, ex_32):
    assert {ex_23, ex_32, ex_32} == {ex_23, ex_32}
