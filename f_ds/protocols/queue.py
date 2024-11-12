from f_ds.protocols.collectionable import ProtocolCollectionable
from typing import Protocol, TypeVar

Item = TypeVar('Item')


class ProtocolQueue(Protocol[Item], ProtocolCollectionable[Item]):
    """
    ============================================================================
     Protocol for a basic Queue.
    ============================================================================
    """

    def pop(self) -> Item:
        """
        ========================================================================
         Pop an Item from the Queue.
        ========================================================================
        """

    def push(self, item: Item) -> None:
        """
        ========================================================================
         Push an Item to the Queue.
        ========================================================================
        """
