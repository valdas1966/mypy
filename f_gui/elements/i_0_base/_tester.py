import pytest
from f_gui.elements.i_0_base.main import Element


@pytest.fixture
def full() -> Element:
    """
    ========================================================================
     Create a full-size Element.
    ========================================================================
    """
    return Element.Factory.full()


@pytest.fixture
def half() -> Element:
    """
    ========================================================================
     Create a centered half-size Element.
    ========================================================================
    """
    return Element.Factory.half()


def test_bounds(full: Element) -> None:
    """
    ========================================================================
     Test the bounds property.
    ========================================================================
    """
    assert full.bounds.to_tuple() == (0, 0, 100, 100)


def test_bounds_half(half: Element) -> None:
    """
    ========================================================================
     Test the bounds of a half-size Element.
    ========================================================================
    """
    assert half.bounds.to_tuple() == (25, 25, 75, 75)


def test_parent(full: Element) -> None:
    """
    ========================================================================
     Test that parent is None by default.
    ========================================================================
    """
    assert full.parent is None


def test_name(full: Element) -> None:
    """
    ========================================================================
     Test the default name.
    ========================================================================
    """
    assert full.name == 'Element'


def test_str(full: Element) -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(full) == 'Element(0, 0, 100, 100)'
