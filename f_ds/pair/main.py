from f_core.mixins.equable import Equable
from typing import Generic, TypeVar

Item = TypeVar('Item')


class Pair(Generic[Item], Equable):
    """
    ============================================================================
     1. Pair of two items.
     2. Can be ordered or unordered.
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

    def key_comparison(self) -> tuple[Item, Item]:
        """
        ========================================================================
         Get the key for comparison of the pair.
        ========================================================================
        """
        if self._is_ordered:
            return self._a, self._b
        else:
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
