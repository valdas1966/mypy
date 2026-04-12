from f_gui.elements.i_0_element.main import Element


def test_bounds() -> None:
    """
    ========================================================================
     Test the bounds property.
    ========================================================================
    """
    assert Element.Factory.full().bounds.to_tuple() == (0, 0, 100, 100)


def test_bounds_half() -> None:
    """
    ========================================================================
     Test the bounds of a half-size Element.
    ========================================================================
    """
    assert Element.Factory.half().bounds.to_tuple() == (25, 25, 75, 75)


def test_parent() -> None:
    """
    ========================================================================
     Test that parent is None by default.
    ========================================================================
    """
    assert Element.Factory.full().parent is None


def test_name() -> None:
    """
    ========================================================================
     Test the default name.
    ========================================================================
    """
    assert Element.Factory.full().name == 'Element'


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(Element.Factory.full()) == 'Element(0, 0, 100, 100)'
