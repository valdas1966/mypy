from f_gui.style.border.main import Border
from f_gui.style.stroke import Stroke, DashPattern


def test_sides_default_none() -> None:
    """
    ========================================================================
     Test that every side defaults to None (no border).
    ========================================================================
    """
    b = Border()
    assert b.top is None
    assert b.left is None
    assert b.bottom is None
    assert b.right is None


def test_per_side() -> None:
    """
    ========================================================================
     Test that an individual side carries its Stroke.
    ========================================================================
    """
    stroke = Stroke(width=3, pattern=DashPattern.DASHED)
    b = Border(top=stroke)
    assert b.top is stroke
    assert b.bottom is None


def test_factory_all() -> None:
    """
    ========================================================================
     Test that Factory.all() sets the same Stroke on all four sides.
    ========================================================================
    """
    stroke = Stroke(width=2)
    b = Border.Factory.all(stroke=stroke)
    assert b.top is stroke
    assert b.left is stroke
    assert b.bottom is stroke
    assert b.right is stroke


def test_str() -> None:
    """
    ========================================================================
     Test the string representation lists only set sides.
    ========================================================================
    """
    b = Border(top=Stroke(width=2))
    assert str(b) == 'Border[T=(2px solid default)]'
