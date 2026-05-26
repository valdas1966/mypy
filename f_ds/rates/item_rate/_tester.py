from f_ds.rates.item_rate import ItemRate


def test_rate() -> None:
    """
    ========================================================================
     Test rate derivation across:
      * mixed counts, positive-only (1.0), negative-only (0.0),
      * zero total -> None.
    ========================================================================
    """
    # Mixed
    kr = ItemRate(item='a', pos=3, neg=1)
    actual = kr.rate
    expected = 0.75
    assert actual == expected

    # Positive only
    kr = ItemRate(item='x', pos=5, neg=0)
    actual = kr.rate
    expected = 1.0
    assert actual == expected

    # Negative only
    kr = ItemRate(item='y', pos=0, neg=7)
    actual = kr.rate
    expected = 0.0
    assert actual == expected

    # Zero total
    kr = ItemRate(item='z', pos=0, neg=0)
    actual = kr.rate
    expected = None
    assert actual == expected


def test_total() -> None:
    """
    ========================================================================
     Test total = pos + neg, including the zero-total case.
    ========================================================================
    """
    # Mixed
    kr = ItemRate(item='a', pos=3, neg=1)
    actual = kr.total
    expected = 4
    assert actual == expected

    # Zero total
    kr = ItemRate(item='z', pos=0, neg=0)
    actual = kr.total
    expected = 0
    assert actual == expected


def test_eq() -> None:
    """
    ========================================================================
     Test equality (Equatable): same rate, total and item.
    ========================================================================
    """
    # Same fields -> equal
    actual = ItemRate(item='a', pos=3, neg=1)
    expected = ItemRate(item='a', pos=3, neg=1)
    assert actual == expected

    # Different item -> not equal
    actual = ItemRate(item='a', pos=3, neg=1)
    expected = ItemRate(item='b', pos=3, neg=1)
    assert actual != expected


def test_order() -> None:
    """
    ========================================================================
     Test ordering (Comparable): higher rate ranks higher;
      ties broken by larger total; None rate ranks lowest.
    ========================================================================
    """
    # Higher rate ranks higher
    actual = ItemRate(item='a', pos=3, neg=1) > ItemRate(item='b', pos=1, neg=3)
    expected = True
    assert actual == expected

    # Equal rate -> larger total ranks higher
    actual = ItemRate(item='q', pos=4, neg=4) > ItemRate(item='p', pos=1, neg=1)
    expected = True
    assert actual == expected

    # None rate ranks lowest
    actual = ItemRate(item='r', pos=0, neg=5) > ItemRate(item='z', pos=0, neg=0)
    expected = True
    assert actual == expected
