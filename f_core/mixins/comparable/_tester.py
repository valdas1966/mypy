from f_core.mixins.comparable import Comparable
import pytest


@pytest.fixture
def a() -> Comparable:
    """
    ========================================================================
     Create a Comparable object with the value 'A'.
    ========================================================================
    """
    return Comparable.Factory.a()

@pytest.fixture
def b() -> Comparable:
    """
    ========================================================================
     Create a Comparable object with the value 'B'.
    ========================================================================
    """
    return Comparable.Factory.b()

def test_eq(a: Comparable, b: Comparable) -> None:
    """
    ========================================================================
     Test the __eq__() method.
    ========================================================================
    """
    assert a == a
    assert not (a == b)


def test_ne(a: Comparable, b: Comparable) -> None:
    """
    ========================================================================
     Test the __ne__() method.
    ========================================================================
    """
    assert a != b
    assert not (a != a)


def test_lt(a: Comparable, b: Comparable) -> None:
    """
    ========================================================================
     Test the __lt__() method.
    ========================================================================
    """
    assert a < b
    assert not (b < a)


def test_le(a: Comparable, b: Comparable) -> None:
    """
    ========================================================================
     Test the __le__() method.
    ========================================================================
    """
    assert a <= a
    assert a <= b
    assert not (b <= a)


def test_gt(a: Comparable, b: Comparable) -> None:
    """
    ========================================================================
     Test the __gt__() method.
    ========================================================================
    """
    assert b > a
    assert not (a > b)


def test_ge(a: Comparable, b: Comparable) -> None:
    """
    ========================================================================
     Test the __ge__() method.
    ========================================================================
    """
    assert a >= a
    assert b >= a
    assert not (a >= b)
