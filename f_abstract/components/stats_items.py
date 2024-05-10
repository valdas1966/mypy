from typing import Generic, TypeVar, Callable, Sequence

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
                 is_spec: Callable[[T], bool]) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        # The Sequence of Items to analyze
        self._items = items
        # A callable that determines whether an item should be in the stats
        self._is_spec = is_spec

    def to_list(self) -> list[T]:
        """
        ========================================================================
         Return a List of Specified-Items that meet the Spec-Condition.
        ========================================================================
        """
        return [item for item in self._items if self._is_spec(item)]
    def count(self) -> int:
        """
        ========================================================================
         Return the count of Specified-Items.
        ========================================================================
        """
        return len(self.to_list())

    def pct(self) -> int:
        """
        ========================================================================
         Return the Percentage of Specified-Items.
        ========================================================================
        """
        if not self._items:
            return 0
        return round(self.count() / len(self._items) * 100, 0)
