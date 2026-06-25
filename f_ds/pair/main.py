from f_core.mixins import Tupleable
from typing import Generic, TypeVar

First = TypeVar('First')
Second = TypeVar('Second')


class Pair(Tupleable, Generic[First, Second]):
    """
    ============================================================================
     Ordered pair of two items — identity is (first, second), via Tupleable.
    ============================================================================
     Heterogeneous: the two slots may differ in type. Equality, ordering,
     hashing, iteration and indexing all derive from the (first, second)
     tuple. Items must be hashable; comparing pairs with `<` additionally
     requires them to be comparable.
    ============================================================================
    """

    # Factory
    Factory: type = None

    def __init__(self,
                 first: First,
                 second: Second) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._first = first
        self._second = second

    @property
    def first(self) -> First:
        """
        ========================================================================
         Get the first item of the pair.
        ========================================================================
        """
        return self._first

    @property
    def second(self) -> Second:
        """
        ========================================================================
         Get the second item of the pair.
        ========================================================================
        """
        return self._second

    def to_tuple(self) -> tuple[First, Second]:
        """
        ========================================================================
         Return the Pair as a (first, second) tuple — the single Tupleable
         method; everything else (eq / order / hash / iter) derives from it.
        ========================================================================
        """
        return self._first, self._second
