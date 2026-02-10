from .main import HasName


def test_str() -> None:
    """
    =======================================================================
     Test the str() function.
    =======================================================================
    """
    a = HasName.Factory.a()
    assert str(a) == 'A'
    empty = HasName()
    assert str(empty) == 'None'


def test_key_comparison() -> None:
    """
    =======================================================================
     Test the key_comparison() method.
    =======================================================================
    """
    a = HasName.Factory.a()
    b = HasName.Factory.b()
    assert HasName.Factory.a() == HasName.Factory.a()
    assert a < b
    assert {a, a, b} == {a, b}


def test_repr() -> None:
    """
    =======================================================================
     Test the repr() function.
    =======================================================================
    """
    a = HasName.Factory.a()
    assert repr(a) == '<HasName: Name=A>'
    class Test(HasName):
        pass
    t = Test(name='T')
    assert repr(t) == '<Test: Name=T>'
