import heapq
from f_data_structure.collections.i_1_queue import QueueBase
from f_abstract.mixins.sortable import Sortable
from typing import TypeVar

T = TypeVar('T', bound=Sortable)


class QueuePriority(QueueBase[T]):
    """
    ============================================================================
     Min-Priority-Queue implemented using heapq module.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init an empty Priority-Queue.
        ========================================================================
        """
        QueueBase.__init__(self)
        self._elements: list[T] = list()

    def push(self, element: T) -> None:
        """
        ========================================================================
         Push an element onto the Priority-Queue. [O(1)]
        ========================================================================
        """
        heapq.heappush(self._elements, element)

    def pop(self) -> T:
        """
        ========================================================================
         Pop and Return the minimal item from the Priority-Queue. [O(n)]
        ========================================================================
        """
        return heapq.heappop(self._elements)
