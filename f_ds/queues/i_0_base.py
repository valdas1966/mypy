from f_ds.collections.i_1d import Collection1D, Item
from abc import abstractmethod


class QueueBase(Collection1D[Item]):
    """
    ============================================================================
     Abstract-Class of Queue.
    ============================================================================
    """

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
