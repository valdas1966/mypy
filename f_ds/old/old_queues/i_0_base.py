from abc import abstractmethod
from typing import Generic, TypeVar
from f_core.mixins.has.name import HasName
from f_ds.mixins.collectionable.main import Collectionable

Item = TypeVar('Item')


class QueueBase(Generic[Item], Collectionable[Item], HasName):
    """
    ============================================================================
     Abstract-Class of Queue.
    ============================================================================
    """

    def __init__(self, name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasName.__init__(self, name=name)

    @abstractmethod
    def push(self, item: Item) -> None:
        """
        ========================================================================
         Push an Element into the Queue.
        ========================================================================
        """
        pass

    @abstractmethod
    def pop(self) -> Item:
        """
        ========================================================================
         Pop an Element from the Queue.
        ========================================================================
        """
        pass

    @abstractmethod
    def peek(self) -> Item:
        """
        ========================================================================
         Return the next Element in the Queue without removing it.
        ========================================================================
        """
        pass

    def update(self) -> None:
        """
        ========================================================================
         Update the Queue.
        ========================================================================
        """
        pass

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Queue.
        ------------------------------------------------------------------------
         Ex: Name[1, 2]
        ========================================================================
        """
        return f'{HasName.__str__(self)}{Collectionable.__str__(self)}'


