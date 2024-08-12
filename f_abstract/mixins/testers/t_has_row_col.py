import pytest
from f_abstract.mixins.has_row_col import HasRowCol


@pytest.fixture
def ex_zero() -> HasRowCol:
    return HasRowCol()

@pytest.fixture
def ex_one() -> HasRowCol:
    return HasRowCol(1)


def test_init(ex_zero, ex_one):
    assert (ex_zero.row, ex_zero.col) == (0, 0)
    assert (ex_one.row, ex_one.col) == (1, 1)


def test_str(ex_zero, ex_one):
    assert str(ex_zero) == '(0,0)'
    assert str(ex_one) == '(1,1)'


def test_neighbors(ex_zero, ex_one):
    assert ex_zero.neighbors() == [HasRowCol(0, 1),
                                    HasRowCol(1, 0)]
    assert ex_one.neighbors() == [HasRowCol(0, 1),
                                  HasRowCol(1, 2),
                                  HasRowCol(2, 1),
                                  HasRowCol(1, 0)]


def test_comparison():
    assert (HasRowCol(0, 0) <
            HasRowCol(0, 1) <
            HasRowCol(1, 0) <
            HasRowCol(1, 1))
    assert HasRowCol() == HasRowCol()
