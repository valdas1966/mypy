import pytest

from f_gui.elements.i_0_element.main import Element
from f_ds.geometry.bounds import Bounds
from f_color.rgb import RGB


class _Concrete(Element):
    """
    ========================================================================
     Minimal concrete subclass — Element itself is abstract.
    ========================================================================
    """
    pass


def test_element_is_abstract() -> None:
    """
    ========================================================================
     Test that Element cannot be instantiated directly.
    ========================================================================
    """
    with pytest.raises(TypeError):
        Element()


def test_subclass_is_instantiable() -> None:
    """
    ========================================================================
     Test that a concrete subclass can be instantiated.
    ========================================================================
    """
    assert isinstance(_Concrete(), Element)


def test_bounds_default() -> None:
    """
    ========================================================================
     Test the default bounds (0, 0, 100, 100).
    ========================================================================
    """
    assert _Concrete().bounds.to_tuple() == (0, 0, 100, 100)


def test_bounds_custom() -> None:
    """
    ========================================================================
     Test custom bounds are stored on the element.
    ========================================================================
    """
    bounds = Bounds(top=25, left=25, bottom=75, right=75)
    assert _Concrete(bounds=bounds).bounds.to_tuple() == (25, 25, 75, 75)


def test_background_default() -> None:
    """
    ========================================================================
     Test that background is None (transparent) by default.
    ========================================================================
    """
    assert _Concrete().background is None


def test_background_set() -> None:
    """
    ========================================================================
     Test that a given background Color is stored on the element.
    ========================================================================
    """
    color = RGB(name='steelblue')
    assert _Concrete(background=color).background is color


def test_parent() -> None:
    """
    ========================================================================
     Test that parent is None by default.
    ========================================================================
    """
    assert _Concrete().parent is None


def test_name() -> None:
    """
    ========================================================================
     Test the default name.
    ========================================================================
    """
    assert _Concrete().name == 'Element'


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(_Concrete()) == 'Element(0, 0, 100, 100)'
