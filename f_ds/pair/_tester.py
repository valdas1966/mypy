from f_ds.pair import Pair


def test_eq() -> None:
    """
    ========================================================================
     Test the __eq__() method.
    ========================================================================
    """
    ab_ordered = Pair.Factory.ab_ordered()
    ab_unordered = Pair.Factory.ab_unordered()
    ba_ordered = Pair.Factory.ba_ordered()
    ba_unordered = Pair.Factory.ba_unordered()
    assert ab_ordered == ab_ordered
    assert ab_unordered == ab_unordered
    assert ab_ordered == ab_unordered
    assert ab_ordered != ba_ordered
    assert ab_unordered == ba_unordered


def test_hash() -> None:
    """
    ========================================================================
     Test the __hash__() method.
    ========================================================================
    """
    ab_ordered = Pair.Factory.ab_ordered()
    ab_unordered = Pair.Factory.ab_unordered()
    ba_ordered = Pair.Factory.ba_ordered()
    ba_unordered = Pair.Factory.ba_unordered()
    assert hash(ab_ordered) == hash(ab_ordered)
    assert hash(ab_unordered) == hash(ab_unordered)
    assert hash(ab_ordered) != hash(ba_ordered)
    assert hash(ab_unordered) == hash(ba_unordered)
    