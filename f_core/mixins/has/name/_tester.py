from f_core.mixins.has.name.main import HasName


def test_str() -> None:
    """
    =======================================================================
     Test the str() function.
    =======================================================================
    """
    a = HasName.Factory.a()
    assert str(a) == 'A'
    empty = HasName()
    assert str(empty) == 'NoName'


def test_repr() -> None:
    """
    =======================================================================
     Test the repr() function.
    =======================================================================
    """
    a = HasName.Factory.a()
    assert repr(a) == '<HasName: A>'
    class Test(HasName):
        pass
    t = Test(name='T')
    assert repr(t) == '<Test: T>'
