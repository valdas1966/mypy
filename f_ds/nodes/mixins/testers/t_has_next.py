from f_ds.nodes.mixins.has_next import HasNext

import pytest


@pytest.fixture
def tail() -> HasNext:
    """
    ========================================================================
     Create a Tail instance for testing.
    ========================================================================
    """
    return HasNext()


@pytest.fixture
def head(tail: HasNext) -> HasNext:
    """
    ========================================================================
     Create a Head instance for testing.
    ========================================================================
    """
    head = HasNext()
    head.next = tail
    return head


def test_has_next(head: HasNext, tail: HasNext) -> None:
    """
    ========================================================================
     Test that HasNext initializes with next=None and can be set.
    ========================================================================
    """
    assert tail.next is None
    assert head.next == tail
