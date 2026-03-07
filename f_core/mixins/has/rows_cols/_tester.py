import pytest
from f_core.mixins.has.rows_cols import HasRowsCols


@pytest.fixture
def square_3() -> HasRowsCols:
    """
    ========================================================================
     Create a HasRowsCols(3, 3) object.
    ========================================================================
    """
    return HasRowsCols.Factory.square_3()


@pytest.fixture
def rect_5_10() -> HasRowsCols:
    """
    ========================================================================
     Create a HasRowsCols(5, 10) object.
    ========================================================================
    """
    return HasRowsCols.Factory.rect_5_10()


def test_rows_cols(rect_5_10: HasRowsCols) -> None:
    """
    ========================================================================
     Test the rows and cols properties.
    ========================================================================
    """
    assert rect_5_10.rows == 5
    assert rect_5_10.cols == 10


def test_square_default(square_3: HasRowsCols) -> None:
    """
    ========================================================================
     Test that cols defaults to rows when not provided.
    ========================================================================
    """
    assert square_3.rows == 3
    assert square_3.cols == 3


def test_cols_zero() -> None:
    """
    ========================================================================
     Test that cols=0 is preserved (not defaulting to rows).
    ========================================================================
    """
    obj = HasRowsCols(rows=3, cols=0)
    assert obj.cols == 0


def test_shape(rect_5_10: HasRowsCols) -> None:
    """
    ========================================================================
     Test the shape() method.
    ========================================================================
    """
    assert rect_5_10.shape() == (5, 10)


def test_str(rect_5_10: HasRowsCols) -> None:
    """
    ========================================================================
     Test the __str__() method.
    ========================================================================
    """
    assert str(rect_5_10) == '(5,10)'


def test_len(rect_5_10: HasRowsCols,
             square_3: HasRowsCols) -> None:
    """
    ========================================================================
     Test the __len__() method.
    ========================================================================
    """
    assert len(rect_5_10) == 50
    assert len(square_3) == 9


def test_is_within(rect_5_10: HasRowsCols) -> None:
    """
    ========================================================================
     Test the is_within() method.
    ========================================================================
    """
    assert rect_5_10.is_within(0, 0)
    assert rect_5_10.is_within(4, 9)
    assert not rect_5_10.is_within(5, 10)
    assert not rect_5_10.is_within(-1, 0)
    assert not rect_5_10.is_within(0, -1)
