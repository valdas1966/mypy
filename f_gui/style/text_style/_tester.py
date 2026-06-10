from f_gui.style.text_style.main import TextStyle
from f_color.rgb import RGB


def test_defaults() -> None:
    """
    ========================================================================
     Test default appearance (monospace, 12px, not bold, no color).
    ========================================================================
    """
    t = TextStyle()
    assert t.font == 'monospace'
    assert t.size == 12
    assert t.bold is False
    assert t.color is None


def test_font() -> None:
    """
    ========================================================================
     Test that the font is stored.
    ========================================================================
    """
    assert TextStyle(font='sans-serif').font == 'sans-serif'


def test_size() -> None:
    """
    ========================================================================
     Test that the size is stored.
    ========================================================================
    """
    assert TextStyle(size=20).size == 20


def test_bold() -> None:
    """
    ========================================================================
     Test that the bold flag is stored.
    ========================================================================
    """
    assert TextStyle(bold=True).bold is True


def test_color() -> None:
    """
    ========================================================================
     Test that the color is stored.
    ========================================================================
    """
    t = TextStyle(color=RGB(name='RED'))
    assert t.color == RGB(name='RED')


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(TextStyle(size=18, bold=True)) == '(monospace 18px bold default)'


def test_factory_title() -> None:
    """
    ========================================================================
     Test the Factory.title() preset.
    ========================================================================
    """
    t = TextStyle.Factory.title()
    assert t.bold is True
    assert t.size == 18
