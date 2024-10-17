import heapq
from f_ds.queues.i_0_base import QueueBase
from f_abstract.mixins.comparable import Comparable
from typing import TypeVar, Iterator

Item = TypeVar('Item', bound=Comparable)


class QueuePriority(QueueBase[Item]):

    def __init__(self):
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        QueueBase.__init__(self)
        self._heap: list[Item] = list()
        self._entry_finder = {}  # Map nodes to entries

    def push(self, item: Item):
        """
        ========================================================================
         Push an item into the heap.
        ========================================================================
        """
        entry = [item.key_comparison(), item]
        self._entry_finder[item] = entry
        heapq.heappush(self._heap, entry)

    def pop(self) -> Item:
        """
        ========================================================================
         Pop and return the smallest item from the heap.
        ========================================================================
        """
        while self._heap:
            _, item = heapq.heappop(self._heap)
            del self._entry_finder[item]
            return item
        raise KeyError("Pop from an empty priority queue")

    def __contains__(self, item: Item) -> bool:
        """
        ========================================================================
         Check if an item is in the priority queue.
        ========================================================================
        """
        return item in self._entry_finder

    def __len__(self) -> int:
        """
        Return the number of items in the priority queue.
        """
        return len(self._entry_finder)

    def update(self, item: Item):
        """
        Update the priority of an existing item by removing and reinserting it.
        This is done by calling remove() and then push().
        """
        self.remove(item)  # Remove the item from the queue
        self.push(item)    # Push it back with the new priority

    def remove(self, item: Item):
        """
        Remove an item from the queue. Rebuild the heap after removal.
        """
        entry = self._entry_finder.pop(item)
        self._heap = [entry for entry in self._heap if entry[-1] != item]
        heapq.heapify(self._heap)  # Rebuild the heap to maintain order

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
