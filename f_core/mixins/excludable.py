from typing import Generic, TypeVar, Sequence

Item = TypeVar('Item')


class Excludable(Generic[Item]):
    """
    ============================================================================
     Mixin provided Exclude-Set functionality for Items.
    ============================================================================
    """

    def __init__(self, exclude: Sequence[Item] = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        self._exclude = set(exclude) if exclude else set()

    def should_exclude(self, item: Item) -> bool:
        """
        ========================================================================
         Return True if the given Item in the Exclude-Set.
        ========================================================================
        """
        return item in self._exclude

    def should_remain(self, item: Item) -> bool:
        """
        ========================================================================
         Return True if the given Item is not in the Exclude-Set.
        ========================================================================
        """
        return not self.should_exclude(item=item)
