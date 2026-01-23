from f_search.ds.frontier.i_1_priority.main import FrontierPriority
from f_search.ds.priority import PriorityG as Priority


def test_abc() -> None:
    """
    ========================================================================
     Test the FrontierPriority.Factory.abc() method.
    ========================================================================
    """
    frontier = FrontierPriority.Factory.abc()
    assert frontier.pop().key == 'C'
    assert frontier.pop().key == 'A'
    assert frontier.pop().key == 'B'


def test_update() -> None:
    """
    ========================================================================
     Test the FrontierPriority.update() method.
    ========================================================================
    """
    frontier = FrontierPriority.Factory.abc_updated()
    assert frontier.pop().key == 'A'


def test_len() -> None:
    """
    ========================================================================
     Test the FrontierPriority.__len__() method.
    ========================================================================
    """
    frontier = FrontierPriority.Factory.abc()
    assert len(frontier) == 3
    frontier.pop()
    assert len(frontier) == 2
    frontier.pop()
    assert len(frontier) == 1
    frontier.pop()
    assert len(frontier) == 0
    frontier = FrontierPriority.Factory.abc_updated()
    assert len(frontier) == 3
