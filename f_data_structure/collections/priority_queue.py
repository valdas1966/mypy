import heapq
from f_data_structure.collections.base.i_0_base import CollectionBase
from typing import Generic, TypeVar

# Define a type variable for the elements stored in SetOrdered
T = TypeVar('T')


class PriorityQueue(Generic[T], CollectionBase[T]):
    """
    ============================================================================
     Desc: Min-Priority-Queue implemented using heapq module.
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init an empty Priority-Queue.
        ========================================================================
        """
        CollectionBase.__init__(self)
        self._elements = list[T]()

    def add(self, element: T) -> None:
        """
        ========================================================================
         Add an element onto the Priority-Queue.
        ========================================================================
        """
        heapq.heappush(self._elements, element)

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
