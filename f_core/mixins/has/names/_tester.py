import pytest
from .main import HasNames, HasName


@pytest.fixture
def abc() -> HasNames:
    """
    ========================================================================
     Create a HasNames object with the names 'A', 'B', and 'C'.
    ========================================================================
    """
    return HasNames.Factory.abc()


def test_names(abc: HasNames) -> None:
    """
    ========================================================================
     Test the names() function.
    ========================================================================
    """
    assert abc.names() == ['A', 'B', 'C']


def test_contains(abc: HasNames) -> None:
    """
    ========================================================================
     Test the __contains__() function.
    ========================================================================
    """
    assert 'A' in abc
    assert 'D' not in abc


def test_getitem(abc: HasNames) -> None:
    """
    ========================================================================
     Test the __getitem__() function.
    ========================================================================
    """
    a, b, c = abc
    assert abc['A'] == a
    assert abc['B'] == b
    assert abc['C'] == c
    assert abc[0] == a
    assert abc[1] == b
    assert abc[2] == c
    assert abc[0:2] == [a, b]
    