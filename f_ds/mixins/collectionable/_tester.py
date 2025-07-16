from .main import Collectionable
import pytest


@pytest.fixture
def abc() -> Collectionable[str]:
    """
    ========================================================================
     Create a Collectionable object with the 'a', 'b', 'c' items.
    ========================================================================
    """
    return Collectionable.Factory.abc()


def test_to_iterable(abc: Collectionable[str]) -> None:
    """
    ========================================================================
     Test the to_iterable() method.
    ========================================================================
    """
    assert abc.to_iterable() == list('abc')


def test_len(abc: Collectionable[str]) -> None:
    """
    ========================================================================
     Test the len() method.
    ========================================================================
    """
    assert len(abc) == 3


def test_contains(abc: Collectionable[str]) -> None:
    """
    ========================================================================
     Test the contains() method.
    ========================================================================
    """
    assert 'a' in abc
    assert 'd' not in abc
