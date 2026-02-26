import pytest
from f_gui.elements.i_1_label.main import Label


@pytest.fixture
def hello() -> Label:
    """
    ========================================================================
     Create a Label with 'Hello' text.
    ========================================================================
    """
    return Label.Factory.hello()


def test_text(hello: Label) -> None:
    """
    ========================================================================
     Test the text property.
    ========================================================================
    """
    assert hello.text == 'Hello'


def test_bounds(hello: Label) -> None:
    """
    ========================================================================
     Test the bounds property.
    ========================================================================
    """
    assert hello.bounds.to_tuple() == (0, 0, 100, 100)


def test_name(hello: Label) -> None:
    """
    ========================================================================
     Test the default name.
    ========================================================================
    """
    assert hello.name == 'Label'


def test_str(hello: Label) -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(hello) == 'Label[Hello](0, 0, 100, 100)'


def test_parent(hello: Label) -> None:
    """
    ========================================================================
     Test that parent is None by default.
    ========================================================================
    """
    assert hello.parent is None
