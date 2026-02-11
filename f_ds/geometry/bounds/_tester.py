from f_ds.geometry.bounds.main import Bounds


def test_full() -> None:
    """
    ========================================================================
     Test the full bounds.
    ========================================================================
    """
    bounds = Bounds.Factory.full()
    assert bounds.to_tuple() == (0, 0, 100, 100)


def test_str() -> None:
    """
    ========================================================================
     Test the string representation of the bounds.
    ========================================================================
    """
    bounds = Bounds.Factory.full()
    assert str(bounds) == '(0, 0, 100, 100)'


def test_repr() -> None:
    """
    ========================================================================
     Test the key comparison of the bounds.
    ========================================================================
    """
    bounds = Bounds.Factory.full()
    assert repr(bounds) == '<Bounds: top=0, left=0, bottom=100, right=100>'
