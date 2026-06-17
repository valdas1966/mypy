from f_gui.style.stroke.main import Stroke, DashPattern
from f_color.rgb import RGB


def test_defaults() -> None:
    """
    ========================================================================
     Test default appearance (no color, 1px, solid).
    ========================================================================
    """
    s = Stroke()
    assert s.color is None
    assert s.width == 1
    assert s.pattern is DashPattern.SOLID


def test_color() -> None:
    """
    ========================================================================
     Test that the color is stored.
    ========================================================================
    """
    s = Stroke(color=RGB(name='RED'))
    assert s.color == RGB(name='RED')


def test_width() -> None:
    """
    ========================================================================
     Test that the width is stored.
    ========================================================================
    """
    assert Stroke(width=4).width == 4


def test_pattern() -> None:
    """
    ========================================================================
     Test that the dash pattern is stored.
    ========================================================================
    """
    assert Stroke(pattern=DashPattern.DOTTED).pattern is DashPattern.DOTTED


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(Stroke(width=2, pattern=DashPattern.DASHED)) == '(2px dashed default)'


def test_factory_dashed() -> None:
    """
    ========================================================================
     Test the Factory.dashed() preset.
    ========================================================================
    """
    s = Stroke.Factory.dashed()
    assert s.pattern is DashPattern.DASHED
    assert s.width == 2
