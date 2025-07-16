from f_ds.mixins.indexable import Indexable
import pytest


@pytest.fixture
def abc() -> Indexable[str]:
    """
    ========================================================================
     Create an Indexable object with the 'a', 'b', 'c' items.
    ========================================================================
    """
    return Indexable.Factory.abc()


def test_int(abc: Indexable[str]) -> None:
    """
    ========================================================================
     Test the __getitem__() method with an integer index.
    ========================================================================
    """
    assert abc[0] == 'a'
    assert abc[1] == 'b'
    assert abc[2] == 'c'


def test_slice(abc: Indexable[str]) -> None:
    """
    ========================================================================
     Test the __getitem__() method with a slice index.
    ========================================================================
    """
    assert abc[0:2] == ['a', 'b']
    assert abc[1:3] == ['b', 'c']
    assert abc[0:3] == ['a', 'b', 'c']
