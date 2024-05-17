from f_ds.collection import CollectionBase, Item
from abc import abstractmethod


class QueueBase(CollectionBase[Item]):
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
