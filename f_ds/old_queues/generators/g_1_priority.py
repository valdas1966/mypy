from f_ds.old_queues.i_1_priority import QueuePriority
from f_core.mixins.generators.g_comparable import GenComparable, Item


class GenPriorityQueue:
    """
    ============================================================================
     Generator for Priority-Queues.
    ============================================================================
    """

    @staticmethod
    def gen_2() -> QueuePriority[Item]:
        """
        ========================================================================
         Generate a Priority-Queue with 2 items.
        ========================================================================
        """
        items = GenComparable.gen_list(length=2)
        queue = QueuePriority()
        for item in items:
            queue.push(item=item)
        return queue
