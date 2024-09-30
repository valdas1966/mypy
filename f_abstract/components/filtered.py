from typing import Generic, TypeVar, Callable, Sequence
from f_abstract.mixins.to_list import ToList, Listable

Item = TypeVar('Item')


class Filtered(Generic[Item], ToList[Item]):
    """
    ============================================================================
     Component-Class for Stats on list Collection based on list spec condition.
    ============================================================================
    """

    def __init__(self,
                 items: Sequence[Item],
                 predicate: Callable[[Item], bool]) -> None:
        """
        ========================================================================
         Init private attributes.
        ========================================================================
        """
        # A callable that determines whether an item is relevant
        self._predicate = predicate
        self._items = items

    def to_list(self) -> Listable[Item]:
        """
        ========================================================================
         Return a List of Items that meet the Predicate.
        ========================================================================
        """
        items = [item for item in self._items if self._predicate(item)]
        return Listable(data=items)

    def pct(self) -> int:
        """
        ========================================================================
         Return the Percentage of Specified-Items.
        ========================================================================
        """
        if not self._items:
            return 0
        return int(round(len(self) / len(self._items) * 100))
