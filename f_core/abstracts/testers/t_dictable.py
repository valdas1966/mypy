from f_core.abstracts.generators.g_dictable import GenDictable


def test_empty() -> None:
    """
    ========================================================================
     Test the empty Dictable object.
    ========================================================================
    """
    d = GenDictable.gen_empty()
    assert d._data == {}


def test_setitem() -> None:
    """
    ========================================================================
     Test the setitem method.
    ========================================================================
    """
    d = GenDictable.gen_empty()
    d['a'] = 1
    d['b'] = 2
    assert d._data == {'a': 1, 'b': 2}


def test_arg() -> None:
    """
    ========================================================================
     Test the Dictable object with arguments.
    ========================================================================
    """
    d = GenDictable.gen_arg()
    assert d._data == {'a': 1, 'b': 2}


def test_getitem() -> None:
    """
    ========================================================================
     Test the getitem method.
    ========================================================================
    """
    d = GenDictable.gen_arg()
    assert d['a'] == 1
    assert d['b'] == 2


def test_contains() -> None:
    """
    ========================================================================
     Test the contains method.
    ========================================================================
    """
    d = GenDictable.gen_arg()
    assert 'a' in d
    assert 'b' in d
    assert 'c' not in d


def test_iter() -> None:
    """
    ========================================================================
     Test the iter method.
    ========================================================================
    """
    d = GenDictable.gen_arg()
    assert list(d) == ['a', 'b']


def test_len() -> None:
    """
    ========================================================================
     Test the len method.
    ========================================================================
    """
    d = GenDictable.gen_arg()
    assert len(d) == 2


def test_str() -> None:
    """
    ========================================================================
     Test the str method.
    ========================================================================
    """
    d = GenDictable.gen_arg()
    assert str(d) == "{'a': 1, 'b': 2}"


def test_get() -> None:
    """
    ========================================================================
     Test the get method.
    ========================================================================
    """ 
    d = GenDictable.gen_arg()
    assert d.get('a') == 1
    assert d.get('b') == 2
    assert d.get('c') is None
    assert d.get('c', 3) == 3


def test_update() -> None:
    """
    ========================================================================
     Test the update method.
    ========================================================================
    """
    d = GenDictable.gen_arg()
    d.update({'c': 3})
    assert d._data == {'a': 1, 'b': 2, 'c': 3}


def test_keys() -> None:
    """
    ========================================================================
     Test the keys method.
    ========================================================================
    """
    d = GenDictable.gen_arg()
    assert d.keys() == ['a', 'b']   
