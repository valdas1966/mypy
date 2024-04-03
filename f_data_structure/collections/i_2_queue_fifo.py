from collections import deque
from f_data_structure.collections.i_1_queue import QueueBase, T
from typing import Deque


class QueueFIFO(QueueBase):
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
        self._elements: Deque[T] = deque()

    def push(self, element: T) -> None:
        """
        ========================================================================
         Push an Element at the end of the Queue. [O(1)]
        ========================================================================
        """
        self._elements.append(element)

    def pop(self) -> T:
        """
        ========================================================================
         Pop the first Element from the Queue. [O(1)]
        ========================================================================
        """
        return self._elements.popleft()
