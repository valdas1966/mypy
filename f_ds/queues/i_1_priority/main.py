import heapq
from typing import Generic, TypeVar,Iterable, Tuple
from f_core.protocols.comparable import Comparable
from f_ds.queues.i_0_base.main import QueueBase, Item

Priority = TypeVar('Priority', bound=Comparable)


class QueuePriority(Generic[Item, Priority],
                    QueueBase[Item]):
    """
    ============================================================================
     Priority Queue implementation using a binary heap.
     Lower priority values = higher priority (min-heap behavior).
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 name: str = 'PriorityQueue') -> None:
        """
        ========================================================================
         Initialize the priority queue with an empty heap.
        ========================================================================
        """
        QueueBase.__init__(self, name=name)
        self._heap: list[Tuple[Comparable, Item]] = []
        self._counter = 0  # To handle items with equal priority (FIFO)

    def push(self, item: Item, priority: Priority = None) -> None:
        """
        ========================================================================
         Push an item with the given priority.
         If priority is None, uses insertion order (FIFO).
         O(log n) time complexity.
        ========================================================================
        """
        if priority is None:
            priority = self._counter        
        # Use counter as tiebreaker to maintain FIFO for equal priorities
        heapq.heappush(self._heap, (priority, self._counter, item))
        self._counter += 1

    def to_iterable(self) -> Iterable[Item]:
        """
        ========================================================================
         Return the Queue's Items in priority order.
         O(n) time complexity.
        ========================================================================
        """
        heap_sorted = sorted(self._heap, key=lambda x: x[0])
        return [item for _, _, item in heap_sorted]


    def pop(self) -> Item:
        """
        ========================================================================
         Remove and return the item with highest priority (lowest value).
         O(log n) time complexity.
        ========================================================================
        """
        _, _, item = heapq.heappop(self._heap)
        return item

    def peek(self) -> Item:
        """
        ========================================================================
         Return the highest priority item without removing it.
         O(1) time complexity.
        ========================================================================
        """
        _, _, item = self._heap[0]
        return item
