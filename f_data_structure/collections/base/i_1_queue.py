from f_data_structure.collections.base.i_0_base import CollectionBase
from typing import Generic, TypeVar
from abc import abstractmethod

T = TypeVar('T')   # Type of Elements in the Queue


class QueueBase(CollectionBase[T]):
    """
    ============================================================================
     Abstract-Class of Queue.
    ============================================================================
    """

    @abstractmethod
    def push(self, element: T) -> None:
        """
        ========================================================================
         Push an Element into the Queue.
        ========================================================================
        """
        pass

    @abstractmethod
    def pop(self) -> T:
        """
        ========================================================================
         Pop an Element from the Queue.
        ========================================================================
        """
        pass
