from typing import Generic, TypeVar, Callable, Sequence, Iterator
from f_abstract.mixins.iterable import Iterable, Item

T = TypeVar('T')


class StatsItems(Generic[T], Iterable[T]):
    """
    ============================================================================
     Component-Class for Stats about a sequence of items based on a
      specified condition.
    ============================================================================
    """

    def __init__(self,
                 items: Sequence[T],
                 predicate: Callable[[T], bool]) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        # The Sequence of Items to analyze
        self._items = items
        # A callable that determines whether an item should be in the stats
        self._predicate = predicate

    def to_list(self) -> list[T]:
        """
        ========================================================================
         Return a list of items that meet the predicate.
        ========================================================================
        """
        return [item for item in self._items if self._predicate(item)]

    def pct(self) -> int:
        """
        ========================================================================
         Return the Percentage of Specified-Items.
        ========================================================================
        """
        if not self._items:
            return 0
        return int(round(len(self) / len(self._items) * 100, 0))
