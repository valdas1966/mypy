import heapq
from f_ds.queues.i_0_base import QueueBase
from f_core.mixins.comparable import Comparable
from typing import TypeVar, Iterable

Item = TypeVar('Item', bound=Comparable)


class QueuePriority(QueueBase[Item]):
    """
    ============================================================================
     Priority-Queue for unique Items.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        QueueBase.__init__(self, name=name)
        self._heap: list[Item] = list()

    def push(self, item: Item) -> None:
        """
        ========================================================================
         Push an item into the Priority-Queue.
        ========================================================================
        """
        heapq.heappush(self._heap, item)

    def pop(self) -> Item:
        """
        ========================================================================
         Pop and return the smallest item from the heap.
        ========================================================================
        """
        return heapq.heappop(self._heap)

    def peek(self) -> Item:
        """
        ========================================================================
         Return the first Item from the Queue without removing it. [O(1)]
        ========================================================================
        """
        return self._heap[0]
    
    def undo_pop(self, item: Item) -> None:
        """
        ========================================================================
         Undo the last Pop-Operation.
        ========================================================================
        """
        self.push(item=item)

    def update(self) -> None:
        """
        ========================================================================
         Updates the Priority-Queue (Heapify).
        ========================================================================
        """
        heapq.heapify(self._heap)

    def to_iterable(self) -> Iterable[Item]:
        """
        ========================================================================
         Return the List of Items (Heap).
        ========================================================================
        """
        return self._heap

