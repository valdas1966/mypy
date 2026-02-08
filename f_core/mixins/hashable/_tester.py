from f_core.mixins.hashable import Hashable


def test_hashable() -> None:
    """
    ========================================================================
     Test the Hashable class.
    ========================================================================
    """
    a = Hashable.Factory.a()
    b = Hashable.Factory.b()
    assert {a, a, b} == {a, b}
