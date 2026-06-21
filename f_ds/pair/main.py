from typing import Generic, TypeVar

from f_core.mixins import Hashable

Item = TypeVar('Item')


class Pair(Hashable, Generic[Item]):
    """
    ============================================================================
     Pair of two items — ordered or unordered. Identity (eq + hash, via
     Hashable) keys on (a, b) when ordered, else on the sorted items, so
     (a, b) and (b, a) match. Unordered mode needs sortable items.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 a: Item,
                 b: Item,
                 is_ordered: bool = False) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._a = a
        self._b = b
        self._is_ordered = is_ordered

    @property
    def a(self) -> Item:
        """
        ========================================================================
         Get the first item of the pair.
        ========================================================================
        """
        return self._a

    @property
    def b(self) -> Item:
        """
        ========================================================================
         Get the second item of the pair.
        ========================================================================
        """
        return self._b

    @property
    def is_ordered(self) -> bool:
        """
        ========================================================================
         Get the order of the pair.
        ========================================================================
        """
        return self._is_ordered

    @property
    def key(self) -> tuple[Item, Item]:
        """
        ========================================================================
         Identity key (drives __eq__ / __hash__): (a, b) when ordered,
         else the sorted items so (a, b) and (b, a) match.
        ========================================================================
        """
        if self._is_ordered:
            return self._a, self._b
        return tuple(sorted((self._a, self._b)))
    
    def __str__(self) -> str:
        """
        ========================================================================
         Get the string representation of the pair.
        ========================================================================
        """
        return f"({self._a}, {self._b})"
    
    def __repr__(self) -> str:
        """
        ========================================================================
         Get the repr representation of the pair.
        ========================================================================
        """
        return f"<Pair: {str(self)}>"
