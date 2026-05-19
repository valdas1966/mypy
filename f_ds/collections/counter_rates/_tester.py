from collections import Counter

from f_ds.collections.counter_rates import CounterRates
from f_ds.collections.key_rate import KeyRate


def test_rows() -> None:
    """
    ========================================================================
     Test row construction and ordering across:
      * shared + positive-only + negative-only keys,
      * a zero-total key (rate None, sorted last),
      * a rate tie broken by larger total.
    ========================================================================
    """
    # Shared + positive-only + negative-only
    cr = CounterRates(positive=Counter(a=3, b=1, c=4),
                       negative=Counter(a=1, b=3, d=2))
    actual = list(cr.rows)
    expected = [KeyRate(item='c', pos=4, neg=0),
                KeyRate(item='a', pos=3, neg=1),
                KeyRate(item='b', pos=1, neg=3),
                KeyRate(item='d', pos=0, neg=2)]
    assert actual == expected

    # Zero-total key sorts after rated rows
    cr = CounterRates(positive=Counter({'z': 0, 'k': 2}),
                       negative=Counter({'z': 0}))
    actual = list(cr.rows)
    expected = [KeyRate(item='k', pos=2, neg=0),
                KeyRate(item='z', pos=0, neg=0)]
    assert actual == expected

    # Rate tie -> larger total first
    cr = CounterRates(positive=Counter(p=1, q=4),
                       negative=Counter(p=1, q=4))
    actual = list(cr.rows)
    expected = [KeyRate(item='q', pos=4, neg=4),
                KeyRate(item='p', pos=1, neg=1)]
    assert actual == expected


def test_len() -> None:
    """
    ========================================================================
     Test __len__ counts distinct keys across both counters.
    ========================================================================
    """
    cr = CounterRates(positive=Counter(a=1, b=1),
                       negative=Counter(b=1, c=1))
    actual = len(cr)
    expected = 3
    assert actual == expected


def test_top() -> None:
    """
    ========================================================================
     Test top(n) returns the n highest-rate rows.
    ========================================================================
    """
    cr = CounterRates(positive=Counter(a=3, b=1, c=4),
                       negative=Counter(a=1, b=3, d=2))
    actual = cr.top(n=2)
    expected = [KeyRate(item='c', pos=4, neg=0),
                KeyRate(item='a', pos=3, neg=1)]
    assert actual == expected


def test_eq() -> None:
    """
    ========================================================================
     Test equality (Equatable): same rows in the same order.
    ========================================================================
    """
    # Same inputs -> equal
    actual = CounterRates(positive=Counter(a=1), negative=Counter(b=1))
    expected = CounterRates(positive=Counter(a=1), negative=Counter(b=1))
    assert actual == expected

    # Different inputs -> not equal
    actual = CounterRates(positive=Counter(a=2), negative=Counter(b=1))
    expected = CounterRates(positive=Counter(a=1), negative=Counter(b=1))
    assert actual != expected
