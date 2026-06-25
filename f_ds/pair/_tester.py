from f_ds.pair import Pair


def test_first_second() -> None:
    """
    ========================================================================
     Test the first and second accessors.
    ========================================================================
    """
    pair = Pair.Factory.ab()
    assert pair.first == 'a'
    assert pair.second == 'b'


def test_eq() -> None:
    """
    ========================================================================
     Test the __eq__() method.
    ========================================================================
    """
    ab = Pair.Factory.ab()
    ba = Pair.Factory.ba()
    assert ab == Pair.Factory.ab()
    assert ab != ba


def test_order() -> None:
    """
    ========================================================================
     Test lexicographic ordering (from Tupleable).
    ========================================================================
    """
    ab = Pair.Factory.ab()
    ba = Pair.Factory.ba()
    assert ab < ba


def test_hash() -> None:
    """
    ========================================================================
     Test the __hash__() method.
    ========================================================================
    """
    ab = Pair.Factory.ab()
    ba = Pair.Factory.ba()
    assert hash(ab) == hash(Pair.Factory.ab())
    assert hash(ab) != hash(ba)


def test_to_tuple() -> None:
    """
    ========================================================================
     Test the to_tuple() method.
    ========================================================================
    """
    assert Pair.Factory.ab().to_tuple() == ('a', 'b')


def test_iter_unpacks() -> None:
    """
    ========================================================================
     Test that a pair unpacks into its two items (from Tupleable).
    ========================================================================
    """
    first, second = Pair.Factory.ab()
    assert (first, second) == ('a', 'b')


def test_heterogeneous() -> None:
    """
    ========================================================================
     Test a pair whose two slots differ in type.
    ========================================================================
    """
    pair = Pair(first='score', second=42)
    assert pair.first == 'score'
    assert pair.second == 42
    assert pair.to_tuple() == ('score', 42)
