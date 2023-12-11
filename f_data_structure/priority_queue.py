import heapq
from typing import TypeVar

T = TypeVar('T')


class PriorityQueue:
    """
    ============================================================================
     Desc: Min-Priority-Queue implemented using heapq module.
    ============================================================================
    """

    def __init__(self):
        """
        ========================================================================
         Desc: Initialize an empty Priority-Queue.
        ========================================================================
        """
        self._items = []

    @property
    def items(self) -> list[T]:
        return self._items.copy()

    def push(self, item: T):
        """
        ========================================================================
         Desc: Push an item onto the Priority-Queue.
        ========================================================================
        """
        heapq.heappush(self._items, item)

    def pop(self) -> T:
        """
        ========================================================================
         Desc: Pop and Return the minimal item from the Priority-Queue.
        ========================================================================
        """
        return heapq.heappop(self._items)

    def __bool__(self) -> bool:
        """
        ========================================================================
         Desc: Return False if the Priority-Queue is empty.
        ========================================================================
        """
        return bool(self._items)

    def __len__(self) -> int:
        """
        ========================================================================
         Desc: Return the number of items on the Priority-Queue.
        ========================================================================
        """
        return len(self._items)

    def __contains__(self, item: T) -> bool:
        return item in self._items
