from f_gui.elements.i_1_label.main import Label


def test_text() -> None:
    """
    ========================================================================
     Test the text property.
    ========================================================================
    """
    assert Label.Factory.hello().text == 'Hello'


def test_bounds() -> None:
    """
    ========================================================================
     Test the bounds property.
    ========================================================================
    """
    assert Label.Factory.hello().bounds.to_tuple() == (0, 0, 100, 100)


def test_name() -> None:
    """
    ========================================================================
     Test the default name.
    ========================================================================
    """
    assert Label.Factory.hello().name == 'Label'


def test_str() -> None:
    """
    ========================================================================
     Test the string representation.
    ========================================================================
    """
    assert str(Label.Factory.hello()) == 'Label[Hello](0, 0, 100, 100)'


def test_parent() -> None:
    """
    ========================================================================
     Test that parent is None by default.
    ========================================================================
    """
    assert Label.Factory.hello().parent is None
