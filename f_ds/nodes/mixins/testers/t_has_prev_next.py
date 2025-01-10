from f_ds.nodes.mixins.has_prev_next import HasPrevNext
import pytest


@pytest.fixture
def head() -> HasPrevNext:
    """
    ========================================================================
     Return a Head object (without a previous object).
    ========================================================================
    """
    return HasPrevNext()


@pytest.fixture
def tail(head: HasPrevNext) -> HasPrevNext:
    """
    ========================================================================
     Return a Tail object (with a previous object).
    ========================================================================
    """
    tail = HasPrevNext()
    tail.prev = head
    return tail


def test_has_prev_next(head: HasPrevNext, tail: HasPrevNext) -> None:
    """
    ========================================================================
     Test the HasPrevNext mixin.
    ========================================================================
    """
    assert head.prev is None
    assert tail.prev is head
    assert head.next is tail
    assert tail.next is None
