from f_core.mixins.equatable.main import Equatable


def test_eq() -> None:
    """
    ========================================================================
     Test the __eq__() method.
    ========================================================================
    """
    a = Equatable.Factory.a()
    b = Equatable.Factory.b()
    assert a == a
    assert a != b
    assert a != 42
    assert a != "A"


def test_ne() -> None:
    """
    ========================================================================
     Test the __ne__() method.
    ========================================================================
    """
    a = Equatable.Factory.a()
    b = Equatable.Factory.b()
    assert a != b
    assert not (a != a)
