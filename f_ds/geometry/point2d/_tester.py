from f_ds.geometry.point2d.main import Point2D


def test_row() -> None:
    """
    ========================================================================
     Test the row property.
    ========================================================================
    """
    p = Point2D(row=3, col=5)
    assert p.row == 3


def test_col() -> None:
    """
    ========================================================================
     Test the col property.
    ========================================================================
    """
    p = Point2D(row=3, col=5)
    assert p.col == 5


def test_to_tuple() -> None:
    """
    ========================================================================
     Test the to_tuple() method.
    ========================================================================
    """
    p = Point2D(row=3, col=5)
    assert p.to_tuple() == (3, 5)


def test_eq() -> None:
    """
    ========================================================================
     Test equality via the (row, col) key.
    ========================================================================
    """
    a = Point2D(row=1, col=2)
    b = Point2D(row=1, col=2)
    assert a == b


def test_hash() -> None:
    """
    ========================================================================
     Test that equal Points hash equally (usable as set/dict keys).
    ========================================================================
    """
    a = Point2D(row=1, col=2)
    b = Point2D(row=1, col=2)
    assert len({a, b}) == 1


def test_unpack() -> None:
    """
    ========================================================================
     Test tuple-unpacking via Tupleable __iter__ (row, col = point).
    ========================================================================
    """
    row, col = Point2D(row=3, col=5)
    assert (row, col) == (3, 5)


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(Point2D(row=3, col=5)) == '(3, 5)'


def test_zero() -> None:
    """
    ========================================================================
     Test the Factory.zero() preset.
    ========================================================================
    """
    assert Point2D.Factory.zero() == Point2D(row=0, col=0)
