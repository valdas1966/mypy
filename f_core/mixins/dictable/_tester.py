from f_core.mixins.dictable import Dictable
import pytest


@pytest.fixture
def abc() -> Dictable[str, int]:
    """
    ========================================================================
     Create a Dictable object with a, b, c keys and 1, 2, 3 values.
    ========================================================================
    """
    return Dictable.Factory.abc()


def test_keys(abc: Dictable[str, int]) -> None:
    """
    ========================================================================
     Test the keys() method.
    ========================================================================
    """
    assert abc.keys() == ['a', 'b', 'c']


def test_values(abc: Dictable[str, int]) -> None:
    """
    ========================================================================
     Test the values() method.
    ========================================================================
    """
    assert abc.values() == [1, 2, 3]


def test_items(abc: Dictable[str, int]) -> None:        
    """
    ========================================================================
     Test the items() method.
    ========================================================================
    """
    assert abc.items() == [('a', 1), ('b', 2), ('c', 3)]


def test_get(abc: Dictable[str, int]) -> None:  
    """
    ========================================================================
     Test the get() method.
    ========================================================================
    """
    assert abc.get('a') == 1
    assert abc.get('d') is None
    assert abc.get('d', 4) == 4


def test_update(abc: Dictable[str, int]) -> None:
    """
    ========================================================================
     Test the update() method.
    ========================================================================
    """
    abc.update({'d': 4})
    assert abc._data == {'a': 1, 'b': 2, 'c': 3, 'd': 4}


def test_getitem(abc: Dictable[str, int]) -> None:
    """
    ========================================================================
     Test the getitem() method.
    ========================================================================
    """
    assert abc['a'] == 1
    assert abc['b'] == 2
    assert abc['c'] == 3


def test_setitem(abc: Dictable[str, int]) -> None:
    """
    ========================================================================
     Test the setitem() method.
    ========================================================================
    """
    abc['d'] = 4
    assert abc._data == {'a': 1, 'b': 2, 'c': 3, 'd': 4}


def test_contains(abc: Dictable[str, int]) -> None:
    """
    ========================================================================
     Test the contains() method.
    ========================================================================
    """
    assert 'a' in abc
    assert 'd' not in abc


def test_len(abc: Dictable[str, int]) -> None:
    """
    ========================================================================
     Test the len() method.
    ========================================================================
    """
    assert len(abc) == 3


def test_iter(abc: Dictable[str, int]) -> None:     
    """
    ========================================================================
     Test the iter() method.
    ========================================================================
    """
    assert list(abc) == ['a', 'b', 'c']


def test_eq(abc: Dictable[str, int]) -> None:
    """
    ========================================================================
     Test the eq() method.
    ========================================================================
    """
    assert abc == abc
    assert abc == Dictable.Factory.abc()
    