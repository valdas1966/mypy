from f_gui.style.stroke.main import Stroke, LineStyle
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
    assert s.style is LineStyle.SOLID


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


def test_style() -> None:
    """
    ========================================================================
     Test that the style is stored.
    ========================================================================
    """
    assert Stroke(style=LineStyle.DOTTED).style is LineStyle.DOTTED


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(Stroke(width=2, style=LineStyle.DASHED)) == '(2px dashed default)'


def test_factory_dashed() -> None:
    """
    ========================================================================
     Test the Factory.dashed() preset.
    ========================================================================
    """
    s = Stroke.Factory.dashed()
    assert s.style is LineStyle.DASHED
    assert s.width == 2
