from typing import Generic, TypeVar, Callable, Sequence
from f_ds.collections.i_1d import Collection1D

T = TypeVar('T')


class StatsItems(Generic[T], Collection1D[T]):
    """
    ============================================================================
     Component-Class for Stats about a Collection based on a spec condition.
    ============================================================================
    """

    def __init__(self,
                 items: Sequence[T],
                 predicate: Callable[[T], bool],
                 name: str = None) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        Collection1D.__init__(self, items=items, name=name)
        # A callable that determines whether an item should be in the stats
        self._predicate = predicate

    def to_list(self) -> list[T]:
        """
        ========================================================================
         Return a list of items that meet the predicate.
        ========================================================================
        """
        return list(filter(self._predicate, self._items))

    def cnt(self) -> int:
        """
        ========================================================================
         Return the number of Specified-Items.
        ========================================================================
        """
        return len(self)

    def pct(self) -> int:
        """
        ========================================================================
         Return the Percentage of Specified-Items.
        ========================================================================
        """
        if not self._items:
            return 0
        return int(round(len(self) / len(self._items) * 100, 0))
