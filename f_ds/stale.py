from typing import Generic, TypeVar, Iterable
from f_ds.entry_priority import EntryPriority
from f_abstract.mixins.comparable import Comparable
from f_ds.mixins.collectionable import Collectionable


Item = TypeVar('Item', bound=Comparable)


class Stale(Generic[Item], Collectionable[EntryPriority]):
    """
    ============================================================================
     Stale objects in Data Structures (not-updated and costly to remove).
    ============================================================================
    """

    def __init__(self) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._stale: set[EntryPriority[Item]] = set()

    def add(self, item: Item) -> None:
        """
        ========================================================================
         Create an EntryPriority by a received Item and Add it into a Stale.
        ========================================================================
        """
        entry = EntryPriority(item=item)
        self._stale.add(entry)

    def to_iterable(self) -> Iterable[EntryPriority[Item]]:
        """
        ========================================================================
         Return Stale-Items as Iterable of EntryPriority.
        ========================================================================
        """
        return self._stale

    def __contains__(self, item: Item) -> bool:
        return EntryPriority(item=item) in self._stale
