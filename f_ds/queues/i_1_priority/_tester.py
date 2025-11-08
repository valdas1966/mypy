from f_ds.queues.i_1_priority.main import QueuePriority


def test_abc() -> None:
    """
    ========================================================================
     Test the QueuePriority.Factory.abc() method.
    ========================================================================
    """
    queue = QueuePriority.Factory.abc()
    assert queue.to_iterable() == ['B', 'C', 'A']
