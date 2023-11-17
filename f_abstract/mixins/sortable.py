from __future__ import annotations


class Sortable:
    """
    ============================================================================
     Mixin Sortable Class.
    ============================================================================
    """

    def key_comparison(self) -> list:
        """
        ========================================================================
         Returns the Object's Key for Sorting.
        ========================================================================
        """
        raise NotImplementedError('key_comparison() must be implemented!')

    def __eq__(self, other: Sortable) -> bool:
        return self.key_comparison() == other.key_comparison()

    def __ne__(self, other: Sortable) -> bool:
        return not self.key_comparison() == other.key_comparison()

    def __lt__(self, other: Sortable) -> bool:
        return self.key_comparison() < other.key_comparison()

    def __le__(self, other: Sortable) -> bool:
        return self.key_comparison() <= other.key_comparison()

    def __gt__(self, other: Sortable) -> bool:
        return self.key_comparison() > other.key_comparison()

    def __ge__(self, other: Sortable) -> bool:
        return self.key_comparison() >= other.key_comparison()
