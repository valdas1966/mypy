from f_ds.nodes.mixins.has_prev import HasPrev
import pytest


@pytest.fixture
def head() -> HasPrev:
    """
    ========================================================================
     Return a Head object (without a previous object).
    ========================================================================
    """
    return HasPrev()


@pytest.fixture
def tail(head: HasPrev) -> HasPrev:
    """
    ========================================================================
     Return a Tail object (with a previous object).
    ========================================================================
    """
    tail = HasPrev()
    tail.prev = head
    return tail


def test_has_prev(head: HasPrev, tail: HasPrev) -> None:
    """
    ========================================================================
     Test that HasPrev initializes with prev=None and can be set.
    ========================================================================
    """
    assert head.prev is None
    assert tail.prev == head

