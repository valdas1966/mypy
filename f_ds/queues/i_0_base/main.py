from abc import abstractmethod
from typing import Generic, TypeVar, Iterable
from f_core.mixins.has.name import HasName
from f_core.mixins.comparable import Comparable
from f_ds.mixins.collectionable.main import Collectionable

Item = TypeVar('Item')


class QueueBase(Generic[Item],
                Collectionable[Item],
                HasName):
    """
    ============================================================================
     Abstract-Class of Queue.
    ============================================================================
    """

    def __init__(self, name: str = 'QueueBase') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)
        Collectionable.__init__(self)

    @abstractmethod
    def to_iterable(self) -> Iterable[Item]:
        """
        ========================================================================
         Convert the Queue's Items into an Iterable.
        ========================================================================
        """
        pass

    def push(self, item: Item, priority: Comparable = None) -> None:
        """
        ========================================================================
         Push an Item into the Queue.
        ========================================================================
        """
        pass

    @abstractmethod
    def pop(self) -> Item:
        """
        ========================================================================
         Pop an Item from the Queue.
        ========================================================================
        """
        pass

    @abstractmethod
    def peek(self) -> Item:
        """
        ========================================================================
         Return the next Item in the Queue without removing it.
        ========================================================================
        """
        pass
