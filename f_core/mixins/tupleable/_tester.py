from f_core.mixins.tupleable import Tupleable
import pytest


@pytest.fixture
def a() -> Tupleable:
    """
    ========================================================================
     Create a Tupleable object with the tuple (1, 2).
    ========================================================================
    """
    return Tupleable.Factory.a()

@pytest.fixture
def b() -> Tupleable:
    """
    ========================================================================
     Create a Tupleable object with the tuple (3, 4).
    ========================================================================
    """
    return Tupleable.Factory.b()


def test_to_tuple(a: Tupleable, b: Tupleable) -> None:
    """
    ========================================================================
     Test the to_tuple() method.
    ========================================================================
    """
    assert a.to_tuple() == (1, 2)
    assert b.to_tuple() == (3, 4)


def test_iter(a: Tupleable) -> None:
    """
    ========================================================================
     Test __iter__() — tuple unpacking and list().
    ========================================================================
    """
    x, y = a
    assert (x, y) == (1, 2)
    assert list(a) == [1, 2]


def test_getitem(a: Tupleable) -> None:
    """
    ========================================================================
     Test __getitem__() — positional indexing.
    ========================================================================
    """
    assert a[0] == 1
    assert a[1] == 2


def test_len(a: Tupleable) -> None:
    """
    ========================================================================
     Test __len__() — number of items in the tuple.
    ========================================================================
    """
    assert len(a) == 2


def test_eq(a: Tupleable, b: Tupleable) -> None:
    """
    ========================================================================
     Test __eq__() — equality by the tuple.
    ========================================================================
    """
    assert a == Tupleable.Factory.a()
    assert a != b


def test_lt(a: Tupleable, b: Tupleable) -> None:
    """
    ========================================================================
     Test __lt__() — lexicographic ordering by the tuple.
    ========================================================================
    """
    assert a < b
    assert not (b < a)


def test_hash(a: Tupleable, b: Tupleable) -> None:
    """
    ========================================================================
     Test __hash__() — equal tuples hash equal; dedup in a set.
    ========================================================================
    """
    assert hash(a) == hash(Tupleable.Factory.a())
    assert len({a, Tupleable.Factory.a(), b}) == 2


def test_repr(a: Tupleable) -> None:
    """
    ========================================================================
     Test __repr__() / __str__() — standardized via HasRepr.
    ========================================================================
    """
    assert str(a) == '(1, 2)'
    assert repr(a) == '<Coord: (1, 2)>'
