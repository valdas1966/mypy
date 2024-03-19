from collections import deque
from f_data_structure.collections.base.i_1_queue import QueueBase
from typing import TypeVar, Deque

T = TypeVar('T')


class QueueFIFO(QueueBase[T]):
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
        self._elements: Deque[T] = deque()

    def push(self, element: T) -> None:
        """
        ========================================================================
         Push an Element into the end of the Queue.
        ========================================================================
        """
        self._elements.append(element)

    def pop(self) -> T:
        """
        ========================================================================
         Pop the first Element from the Queue.
        ========================================================================
        """
        return self._elements.popleft()
