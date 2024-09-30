import heapq
from f_ds.queues.i_0_base import QueueBase, Listable
from f_abstract.mixins.sortable import Sortable
from typing import TypeVar

Item = TypeVar('Item', bound=Sortable)


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

    def to_list(self) -> Listable[Item]:
        """
        ========================================================================
         Convert the Queue into List in Priority order.
        ========================================================================
        """
        return Listable(data=self._items)
