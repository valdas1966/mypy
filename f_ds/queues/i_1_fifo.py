from collections import deque
from f_ds.mixins.collectionable.main import IterableSized
from f_ds.queues.i_0_base import QueueBase, Item
from typing import Deque


class QueueFIFO(QueueBase[Item]):
    """
    ============================================================================
     FIFO (First In - First Out) Queue.
    ============================================================================
    """

    def __init__(self, name: str = 'QueueFifo') -> None:
        """
        ========================================================================
         Init with an empty Queue.
        ========================================================================
        """
        QueueBase.__init__(self, name=name)
        self._items: Deque[Item] = deque()

    def push(self, item: Item) -> None:
        """
        ========================================================================
         Push an Item at the end of the Queue. [O(1)]
        ========================================================================
        """
        self._items.append(item)

    def pop(self) -> Item:
        """
        ========================================================================
         Pop the first Item from the Queue. [O(1)]
        ========================================================================
        """
        return self._items.popleft()

    def peek(self) -> Item:
        """
        ========================================================================
         Return the first Item from the Queue without removing it. [O(1)]
        ========================================================================
        """
        return self._items[0]
    
    def undo_pop(self, item: Item) -> None:
        """
        ========================================================================
         Undo the last Pop-Operation.
        ========================================================================
        """
        self._items.appendleft(item)

    def to_list(self) -> list[Item]:
        """
        ========================================================================
         Convert Queue's Items into an ordered List of Items.
        ========================================================================
        """
        return list(self._items)

    def to_iterable(self) -> IterableSized:
        return self._items
