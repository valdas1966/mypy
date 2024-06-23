from typing import Generic, TypeVar, Callable, Sequence, Iterator
from f_utils import u_list

T = TypeVar('T')


class StatsItems(Generic[T]):
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

    def cnt(self) -> int:
        """
        ========================================================================
         Return the count of Specified-Items.
        ========================================================================
        """
        return len(list(self))

    def pct(self) -> int:
        """
        ========================================================================
         Return the Percentage of Specified-Items.
        ========================================================================
        """
        if not self._items:
            return 0
        return int(round(self.cnt() / len(self._items) * 100, 0))

    def __iter__(self) -> Iterator[T]:
        """
        ========================================================================
         Iterate over the Items that meet the Predicate.
        ========================================================================
        """
        return (item for item in self._items if self._predicate(item))
