import heapq
from f_ds.queues.i_0_base import QueueBase
from f_abstract.mixins.comparable import Comparable
from typing import TypeVar, Iterator

Item = TypeVar('Item', bound=Comparable)


class QueuePriority(QueueBase[Item]):
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
        self._items: list[Item] = list()

    def push(self, item: Item) -> None:
        """
        ========================================================================
         Push an element onto the Priority-Queue. O(n)
        ========================================================================
        """
        heapq.heappush(self._items, item)

    def pop(self) -> Item:
        """
        ========================================================================
         Pop and Return the Minimal-Item from the Priority-Queue. O(1)
        ========================================================================
        """
        return heapq.heappop(self._items)

    def __iter__(self) -> Iterator[Item]:
        """
        ========================================================================
         Allow iterate over the Queue-Objects in priority order.
        ========================================================================
        """
        return iter(sorted(self._items))
