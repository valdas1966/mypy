from .main import HasName


def test_str() -> None:
    """
    =======================================================================
     Test the str() function.
    =======================================================================
    """
    a = HasName.Factory.a()
    assert str(a) == 'A'
    empty = HasName.Factory.empty()
    assert str(empty) == 'None'
    none = HasName.Factory.none()
    assert str(none) == 'None'


def test_key_comparison() -> None:
    """
    =======================================================================
     Test the key_comparison() method.
    =======================================================================
    """
    a = HasName.Factory.a()
    empty = HasName.Factory.empty()
    none = HasName.Factory.none()
    assert empty < a
    assert empty == none
