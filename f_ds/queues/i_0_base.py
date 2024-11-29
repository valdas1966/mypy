from abc import abstractmethod
from typing import Generic, TypeVar
from f_core.mixins.nameable import Nameable
from f_ds.mixins.collectionable import Collectionable

Item = TypeVar('Item')


class QueueBase(Generic[Item], Collectionable[Item], Nameable):
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
        Nameable.__init__(self, name=name)

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

    def __str__(self) -> str:
        """
        ========================================================================
         Return STR-REPR of the Queue.
        ------------------------------------------------------------------------
         Ex: Name[1, 2]
        ========================================================================
        """
        return f'{Nameable.__str__(self)}{Collectionable.__str__(self)}'
