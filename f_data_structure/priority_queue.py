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
         Desc: Initialize empty Priority-Queue.
        ========================================================================
        """
        self._items = []

    def push(self, item: T):
        """
        ========================================================================
         Desc: Push item onto the Priority-Queue.
        ========================================================================
        """
        heapq.heappush(self._items, item)

    def pop(self) -> T:
        """
        ========================================================================
         Desc: Pop and Return the minimal item in the Priority-Queue.
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
