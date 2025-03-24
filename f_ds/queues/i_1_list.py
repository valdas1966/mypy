from f_ds.queues.i_0_base import QueueBase
from enum import Enum, auto
from typing import TypeVar, Iterable

Item = TypeVar('Item')


class TypePriority(Enum):
        """
        ========================================================================
         Type of Priority.
        ========================================================================
        """
        MIN = auto()
        MAX = auto()

class QueueList(QueueBase[Item]):
    """
    ============================================================================
     Queue-Class based on List.
    ============================================================================
    """

    def __init__(self,
                 name: str = None,
                 priority: TypePriority = TypePriority.MIN) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        QueueBase.__init__(self, name=name)
        self._items: list[Item] = list()
        self._priority: TypePriority = priority

    def push(self, item: Item) -> None:
        """
        ========================================================================
         Push an Element into the Queue.
        ========================================================================
        """
        self._items.append(item)    

    def pop(self) -> Item:
        """
        ========================================================================
         Pop an Element from the Queue.
        ========================================================================
        """
        self.update()
        return self._items.pop(0)

    def peek(self) -> Item:
        """
        ========================================================================
         Return the next Element in the Queue without removing it.
        ========================================================================
        """
        self.update()
        return self._items[0]
    
    def update(self) -> None:
        """
        ========================================================================
         Update the Queue.
        ========================================================================
        """
        if self._priority == TypePriority.MIN:
            self._items.sort()
        else:
            self._items.sort(reverse=True)

    def to_iterable(self) -> Iterable[Item]:
        """
        ========================================================================
         Return the Items of the Queue as an Iterable.
        ========================================================================
        """
        return self._items  
