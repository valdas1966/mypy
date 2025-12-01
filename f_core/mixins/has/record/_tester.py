from f_core.mixins.has.record.main import HasRecord


def test_a() -> None:
    """
    ========================================================================
     Test of the Factory of A.
    ========================================================================
    """
    a = HasRecord.Factory.a()
    assert a.record == {'name': 'A', 'a': 1}
    assert a.str_record() == '[name=A] [a=1]'


def test_b() -> None:
    """
    ========================================================================
     Test of the Factory of B.
    ========================================================================
    """
    b = HasRecord.Factory.b()
    assert b.record == {'name': 'B', 'a': 1, 'b': 2}
    assert b.str_record() == '[name=B] [a=1] [b=2]'

def test_none() -> None:
    """
    ========================================================================
     Test of the Factory of None.
    ========================================================================
    """
    none = HasRecord.Factory.none()
    assert none.record == {}
    assert none.str_record() == str()
