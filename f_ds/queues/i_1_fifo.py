from collections import deque
from f_ds.queues.i_0_base import QueueBase, Item
from typing import Deque


class QueueFIFO(QueueBase[Item]):
    """
    ============================================================================
     FIFO (First In - First Out) Queue.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init with an empty Queue.
        ========================================================================
        """
        QueueBase.__init__(self)
        self._items: Deque[Item] = deque()

    def push(self, item: Item) -> None:
        """
        ========================================================================
         Push an Item at the end of the Queue. [O(1)]
        ========================================================================
        """
        self._items.append(item)

    def pop(self) -> Item:
        """
        ========================================================================
         Pop the first Item from the Queue. [O(1)]
        ========================================================================
        """
        return self._items.popleft()
