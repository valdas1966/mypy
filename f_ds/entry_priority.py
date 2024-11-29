from f_core.mixins.comparable import Comparable
from f_core.mixins.equable import Equable
from typing import Generic, TypeVar

Item = TypeVar('Item', bound=Comparable)


class EntryPriority(Generic[Item], Equable):
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

    def key_comparison(self) -> list:
        """
        ========================================================================
         Return the Entry Comparison-Key.
        ========================================================================
        """
        return [str(self._item)] + self._item.key_comparison()

    def __hash__(self) -> int:
        """
        ========================================================================
         Hash by Object's Name + Key_Comparison.
        ========================================================================
        """
        return hash(tuple(self.key_comparison()))
