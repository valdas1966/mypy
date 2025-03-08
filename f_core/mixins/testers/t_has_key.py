from f_core.mixins.generators.g_has_key import GenHasKey


def test_comparable() -> None:
    """
    ========================================================================
     Test the Comparable mixin.
    ========================================================================
    """
    one = GenHasKey.one()
    two = GenHasKey.two()
    assert one < two
    assert one <= two
    assert two > one
    assert two >= one
    assert one == one
    assert one != two


def test_hash() -> None:
    """
    ========================================================================
     Test the Hash mixin.
    ========================================================================
    """
    one = GenHasKey.one()
    two = GenHasKey.two()
    assert hash(one) == hash(one)
    assert hash(one) != hash(two)
    assert {one, one} == {one}
    assert {one, two} == {one, two}
