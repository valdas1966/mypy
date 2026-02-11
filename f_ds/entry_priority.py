from f_core.mixins.comparable import Comparable
from f_core.mixins.equatable.main import Equatable
from typing import Generic, TypeVar

Item = TypeVar('Item', bound=Comparable)


class EntryPriority(Generic[Item], Equatable):
    """
    ============================================================================
     Entry for Item with Priority.
    ============================================================================
    """

    def __init__(self, item: Item) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._item = item

    def key(self) -> list:
        """
        ========================================================================
         Return the Entry Comparison-Key.
        ========================================================================
        """
        return [str(self._item)] + self._item.key()

    def __hash__(self) -> int:
        """
        ========================================================================
         Hash by Object's Name + Key_Comparison.
        ========================================================================
        """
        return hash(tuple(self.key()))
