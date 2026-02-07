from f_core.mixins.equable.main import Equable


def test_eq() -> None:
    """
    ========================================================================
     Test the __eq__() method.
    ========================================================================
    """
    a = Equable.Factory.a()
    b = Equable.Factory.b()
    assert a == a
    assert a != b


def test_ne() -> None:
    """
    ========================================================================
     Test the __ne__() method.
    ========================================================================
    """
    a = Equable.Factory.a()
    b = Equable.Factory.b()
    assert a != b
    assert not (a != a)
