from f_data_structure.collections.i_0_base import CollectionBase, T
from abc import abstractmethod


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
