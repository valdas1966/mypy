from __future__ import annotations
from typing import Generic, TypeVar, Callable, TYPE_CHECKING

if TYPE_CHECKING:  # only for type checkers; avoids runtime cycle
    from f_ds.groups.main import Group

Item = TypeVar('Item')


class Random(Generic[Item]):
    """
    ============================================================================
     Random Class for Groups.
    ============================================================================
    """

    def __init__(self, group: 'Group[Item]') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._group = group

    def item(self,
             epochs: int = 100,
             predicate: Callable[[Item], bool] = None) -> Item:
        """
        ========================================================================
         Return a random item from the group that meets the predicate.
         If no item meets the predicate (after {epochs} epochs), return None.
        ========================================================================
        """
        for _ in range(epochs):
            item = self._group.sample(size=1)[0]
            if predicate:
                if predicate(item):
                    return item
            else:
                return item
        return None

