from f_ds.set_ordered import SetOrdered


def test_add() -> None:
    """
    ========================================================================
     Test add() method.
    ========================================================================
    """
    s = SetOrdered()
    assert 1 not in s
    s.add(1)
    assert 1 in s


def test_add_duplicate() -> None:
    """
    ========================================================================
     Test that adding a duplicate does not increase size.
    ========================================================================
    """
    s = SetOrdered()
    s.add(1)
    assert len(s) == 1
    s.add(1)
    assert len(s) == 1


def test_discard() -> None:
    """
    ========================================================================
     Test discard() method.
    ========================================================================
    """
    s = SetOrdered()
    s.add(1)
    assert len(s) == 1
    s.discard(1)
    assert len(s) == 0
    s.discard(1)
    assert len(s) == 0


def test_contains() -> None:
    """
    ========================================================================
     Test __contains__() method.
    ========================================================================
    """
    s = SetOrdered()
    s.add(1)
    assert 1 in s
    assert 2 not in s


def test_len() -> None:
    """
    ========================================================================
     Test __len__() method.
    ========================================================================
    """
    assert len(SetOrdered()) == 0
    assert len(SetOrdered.Factory.abc()) == 3


def test_bool() -> None:
    """
    ========================================================================
     Test __bool__() method.
    ========================================================================
    """
    assert not SetOrdered()
    assert SetOrdered.Factory.abc()


def test_init_duplicates() -> None:
    """
    ========================================================================
     Test that duplicates in iterable are removed.
    ========================================================================
    """
    s = SetOrdered([1, 2, 2, 3, 1])
    assert len(s) == 3


def test_order_preserved() -> None:
    """
    ========================================================================
     Test that iteration order matches insertion order.
    ========================================================================
    """
    s = SetOrdered()
    s.add(3)
    s.add(1)
    s.add(2)
    assert list(s) == [3, 1, 2]


def test_order_after_discard() -> None:
    """
    ========================================================================
     Test that order is preserved after discard.
    ========================================================================
    """
    s = SetOrdered([1, 2, 3, 4])
    s.discard(2)
    assert list(s) == [1, 3, 4]


def test_readd_appends_to_end() -> None:
    """
    ========================================================================
     Test that re-adding a discarded item appends to end.
    ========================================================================
    """
    s = SetOrdered([1, 2, 3])
    s.discard(1)
    s.add(1)
    assert list(s) == [2, 3, 1]


def test_union() -> None:
    """
    ========================================================================
     Test union (|) operator.
    ========================================================================
    """
    assert SetOrdered([1, 2]) | SetOrdered([2, 3]) == SetOrdered([1, 2, 3])


def test_intersection() -> None:
    """
    ========================================================================
     Test intersection (&) operator.
    ========================================================================
    """
    assert SetOrdered([1, 2]) & SetOrdered([2, 3]) == SetOrdered([2])


def test_difference() -> None:
    """
    ========================================================================
     Test difference (-) operator.
    ========================================================================
    """
    assert SetOrdered([1, 2]) - SetOrdered([2, 3]) == SetOrdered([1])


def test_subset() -> None:
    """
    ========================================================================
     Test subset (<=) operator.
    ========================================================================
    """
    assert SetOrdered([1, 2]) < SetOrdered([1, 2, 3])


def test_repr_small() -> None:
    """
    ========================================================================
     Test repr for small set.
    ========================================================================
    """
    assert repr(SetOrdered.Factory.abc()) == "SetOrdered(['a', 'b', 'c'])"


def test_repr_large() -> None:
    """
    ========================================================================
     Test repr truncation for large set.
    ========================================================================
    """
    r = repr(SetOrdered(list(range(100))))
    assert r == "SetOrdered(0, 1, 2, ..., 99, len=100)"
