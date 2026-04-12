from f_ds.queues.i_1_indexed.main import QueueIndexed


class Factory:
    """
    ========================================================================
     Factory for QueueIndexed test instances.
    ========================================================================
    """

    @staticmethod
    def empty() -> QueueIndexed:
        """
        ====================================================================
         Empty Indexed Heap.
        ====================================================================
        """
        return QueueIndexed()

    @staticmethod
    def abc() -> QueueIndexed:
        """
        ====================================================================
         Heap with 3 items: A(3), B(1), C(2).
         Pop order: B, C, A.
        ====================================================================
        """
        q = QueueIndexed()
        q.push(item='A', priority=(3,))
        q.push(item='B', priority=(1,))
        q.push(item='C', priority=(2,))
        return q
