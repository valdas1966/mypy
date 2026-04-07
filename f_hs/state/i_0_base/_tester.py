import pytest
from f_hs.state import StateBase


@pytest.fixture
def a() -> StateBase[str]:
    """
    ========================================================================
     Create a StateBase with key 'A'.
    ========================================================================
    """
    return StateBase.Factory.a()


@pytest.fixture
def b() -> StateBase[str]:
    """
    ========================================================================
     Create a StateBase with key 'B'.
    ========================================================================
    """
    return StateBase.Factory.b()


def test_key(a: StateBase[str]) -> None:
    """
    ========================================================================
     Test the key property.
    ========================================================================
    """
    assert a.key == 'A'


def test_eq(a: StateBase[str]) -> None:
    """
    ========================================================================
     Test equality between two StateBase with the same key.
    ========================================================================
    """
    other = StateBase.Factory.a()
    assert a == other


def test_neq(a: StateBase[str], b: StateBase[str]) -> None:
    """
    ========================================================================
     Test inequality between two StateBase with different keys.
    ========================================================================
    """
    assert a != b


def test_hash(a: StateBase[str]) -> None:
    """
    ========================================================================
     Test hash consistency with equality.
    ========================================================================
    """
    other = StateBase.Factory.a()
    assert hash(a) == hash(other)


def test_str(a: StateBase[str]) -> None:
    """
    ========================================================================
     Test string representation.
    ========================================================================
    """
    assert str(a) == 'A'


def test_repr(a: StateBase[str]) -> None:
    """
    ========================================================================
     Test repr representation.
    ========================================================================
    """
    assert repr(a) == '<StateBase: Key=A>'
