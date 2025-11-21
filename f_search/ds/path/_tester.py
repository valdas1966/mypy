from f_search.ds.path._factory import Path, StateBase


def test_to_iterable() -> None:
    """
    ========================================================================
     Test the to_iterable() method.
    ========================================================================
    """
    zero = StateBase.Factory.zero()
    one = StateBase.Factory.one()
    two = StateBase.Factory.two()
    path = Path.Factory.diagonal()
    assert path.to_iterable() == [zero, one, two]


def test_head() -> None:
    """
    ========================================================================
    Test the head() method.
    ========================================================================
    """
    zero = StateBase.Factory.zero()
    path = Path.Factory.diagonal()
    assert path.head() == zero


def test_tail() -> None:
    """
    ========================================================================
    Test the tail() method.
    ========================================================================
    """
    two = StateBase.Factory.two()
    path = Path.Factory.diagonal()
    assert path.tail() == two


def test_reverse() -> None:
    """
    ========================================================================
    Test the reverse() method.
    ========================================================================
    """
    zero = StateBase.Factory.zero()
    one = StateBase.Factory.one()
    two = StateBase.Factory.two()
    path = Path.Factory.diagonal()
    assert path.reverse() == Path(states=[two, one, zero])


def test_add() -> None:
    """
    ========================================================================
    Test the add() method.
    ========================================================================
    """
    zero = StateBase.Factory.zero()
    one = StateBase.Factory.one()
    two = StateBase.Factory.two()
    path_1 = Path.Factory.diagonal()
    path_2 = Path.Factory.diagonal()
    assert path_1 + path_2 == Path(states=[zero, one, two, zero, one, two]) 


def test_iadd() -> None:
    """
    ========================================================================
    Test the iadd() method.
    ========================================================================
    """
    zero = StateBase.Factory.zero()
    one = StateBase.Factory.one()
    two = StateBase.Factory.two()
    path = Path.Factory.diagonal()
    path += path
    assert path == Path(states=[zero, one, two, zero, one, two])    
