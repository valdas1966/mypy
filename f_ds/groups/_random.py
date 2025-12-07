from f_ds.groups.group import Group, Item
from typing import Callable


class Random:
    """
    ============================================================================
     Random Class for Groups.
    ============================================================================
    """

    def __init__(self, group: Group) -> None:
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
            item = self._group.sample(size=1)
            if predicate(item):
                return item            
        return None

