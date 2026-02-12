from f_core.mixins.hashable import Hashable


def test_hashable() -> None:
    """
    ========================================================================
     Test the Hashable class.
    ========================================================================
    """
    a = Hashable.Factory.a()
    b = Hashable.Factory.b()
    a_other = Hashable.Factory.a()  # distinct instance, same key
    # Value-based equality
    assert a == a_other
    assert a != b
    # Hash consistency
    assert hash(a) == hash(a_other)
    # Set deduplication (value-based, not identity-based)
    assert {a, a_other, b} == {a, b}
