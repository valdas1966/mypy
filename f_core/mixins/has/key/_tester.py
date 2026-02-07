from f_core.mixins.has.key import HasKey


def test_a() -> None:
    """
    ========================================================================
    """
    a = HasKey.Factory.a()
    other_a = HasKey.Factory.a()
    assert a.key == 'A'
    assert a.key_comparison() == 'A'
    assert hash(a) == hash('A')
    assert a == other_a
    