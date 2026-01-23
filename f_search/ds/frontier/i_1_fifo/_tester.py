from f_search.ds.frontier.i_1_fifo import FrontierFifo


def test_pop() -> None:
    """
    ========================================================================
     Test the FrontierFifo.pop() method.
    ========================================================================
    """
    frontier = FrontierFifo.Factory.abc()
    assert frontier.pop() == 'A'
    assert frontier.pop() == 'B'
    assert frontier.pop() == 'C'


def test_peek() -> None:
    """
    ========================================================================
     Test the FrontierFifo.peek() method.
    ========================================================================
    """
    frontier = FrontierFifo.Factory.abc()
    assert frontier.peek() == 'A'
    assert frontier.pop() == 'A'

def test_len() -> None:
    """
    ========================================================================
     Test the FrontierFifo.len() method.
    ========================================================================
    """
    frontier = FrontierFifo.Factory.abc()
    assert len(frontier) == 3


def test_contains() -> None:
    """
    ========================================================================
     Test the FrontierFifo.contains() method.
    ========================================================================
    """
    frontier = FrontierFifo.Factory.abc()
    assert 'A' in frontier
    assert 'B' in frontier
    assert 'C' in frontier
    assert 'D' not in frontier  


def test_bool() -> None:
    """
    ========================================================================
     Test the FrontierFifo.bool() method.
    ========================================================================
    """
    frontier = FrontierFifo.Factory.abc()
    assert bool(frontier)
    frontier.pop()
    frontier.pop()      
    frontier.pop()
    assert not bool(frontier)


def test_iter() -> None:
    """
    ========================================================================
     Test the FrontierFifo.iter() method.
    ========================================================================
    """
    frontier = FrontierFifo.Factory.abc()
    assert list(frontier) == ['A', 'B', 'C']    


def test_str() -> None:
    """
    ========================================================================
     Test the FrontierFifo.str() method.
    ========================================================================
    """
    frontier = FrontierFifo.Factory.abc()
    assert str(frontier) == "['A', 'B', 'C']"
