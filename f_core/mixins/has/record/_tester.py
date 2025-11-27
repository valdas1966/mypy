from f_core.mixins.has.record.main import HasRecord


def test_a() -> None:
    """
    ========================================================================
     Test of the Factory of A.
    ========================================================================
    """
    a = HasRecord.Factory.a()
    assert a.record == {'a': 1}


def test_b() -> None:
    """
    ========================================================================
     Test of the Factory of B.
    ========================================================================
    """
    b = HasRecord.Factory.b()
    assert b.record == {'a': 1, 'b': 2}


def test_none() -> None:
    """
    ========================================================================
     Test of the Factory of None.
    ========================================================================
    """
    none = HasRecord.Factory.none()
    assert none.record == {}
