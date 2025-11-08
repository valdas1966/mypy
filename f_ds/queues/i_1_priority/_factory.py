from f_ds.queues.i_1_priority.main import QueuePriority


class Factory:
    """
    ============================================================================
     Factory for creating QueuePriority objects.
    ============================================================================
    """

    @staticmethod
    def abc() -> QueuePriority[str, int]:
        """
        ========================================================================
         Generate a QueuePriority with the 'A', 'B', 'C' items and
          mess inserted priorities.
        ========================================================================
        """
        queue = QueuePriority[str, int]()
        queue.push(item='A', priority=3)
        queue.push(item='B', priority=1)
        queue.push(item='C', priority=2)
        return queue
