from f_ds.queues.i_1_indexed import QueueIndexed


def test_push_pop_order() -> None:
    """
    ========================================================================
     Test that pop returns items in priority order.
    ========================================================================
    """
    q = QueueIndexed.Factory.abc()
    assert q.pop() == 'B'
    assert q.pop() == 'C'
    assert q.pop() == 'A'


def test_len() -> None:
    """
    ========================================================================
     Test __len__ returns correct size.
    ========================================================================
    """
    q = QueueIndexed.Factory.abc()
    assert len(q) == 3
    q.pop()
    assert len(q) == 2


def test_bool() -> None:
    """
    ========================================================================
     Test __bool__ returns True when non-empty, False when empty.
    ========================================================================
    """
    q = QueueIndexed.Factory.empty()
    assert not q
    q.push(item='X', priority=(1,))
    assert q


def test_contains() -> None:
    """
    ========================================================================
     Test __contains__ checks membership.
    ========================================================================
    """
    q = QueueIndexed.Factory.abc()
    assert 'A' in q
    assert 'Z' not in q
    q.pop()
    assert 'B' not in q


def test_peek() -> None:
    """
    ========================================================================
     Test peek returns min without removing.
    ========================================================================
    """
    q = QueueIndexed.Factory.abc()
    assert q.peek() == 'B'
    assert len(q) == 3


def test_decrease_key() -> None:
    """
    ========================================================================
     Test decrease_key changes the pop order.
    ========================================================================
    """
    q = QueueIndexed()
    q.push(item='A', priority=(5,))
    q.push(item='B', priority=(3,))
    q.push(item='C', priority=(4,))
    # A has highest priority (5). Decrease to (1).
    q.decrease_key(item='A', priority=(1,))
    assert q.pop() == 'A'
    assert q.pop() == 'B'
    assert q.pop() == 'C'


def test_decrease_key_no_op() -> None:
    """
    ========================================================================
     Test decrease_key is a no-op when new priority is not better.
    ========================================================================
    """
    q = QueueIndexed()
    q.push(item='A', priority=(1,))
    q.push(item='B', priority=(2,))
    q.decrease_key(item='A', priority=(5,))
    assert q.pop() == 'A'


def test_push_existing_item() -> None:
    """
    ========================================================================
     Test push with existing item calls decrease_key.
    ========================================================================
    """
    q = QueueIndexed()
    q.push(item='A', priority=(5,))
    q.push(item='B', priority=(3,))
    # Push A again with better priority
    q.push(item='A', priority=(1,))
    assert len(q) == 2
    assert q.pop() == 'A'


def test_clear() -> None:
    """
    ========================================================================
     Test clear removes all items.
    ========================================================================
    """
    q = QueueIndexed.Factory.abc()
    q.clear()
    assert len(q) == 0
    assert not q


def test_tuple_priority_tiebreak() -> None:
    """
    ========================================================================
     Test tuple priorities with tie-breaking (f, -g).
    ========================================================================
    """
    q = QueueIndexed()
    q.push(item='shallow', priority=(4, -1))
    q.push(item='deep', priority=(4, -3))
    # Same f=4, but deep has -g=-3 < -g=-1 → popped first
    assert q.pop() == 'deep'
    assert q.pop() == 'shallow'


def test_to_iterable() -> None:
    """
    ========================================================================
     Test to_iterable returns items in priority order.
    ========================================================================
    """
    q = QueueIndexed.Factory.abc()
    items = list(q.to_iterable())
    assert items == ['B', 'C', 'A']
