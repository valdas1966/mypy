from __future__ import annotations


class Comparable:
    """
    ============================================================================
     Mixin Comparable Class.
    ============================================================================
    """

    def key_comparison(self) -> list:
        """
        ========================================================================
         Returns the Object's Key for Sorting.
        ========================================================================
        """
        raise NotImplementedError('key_comparison() must be implemented!')

    def __eq__(self, other: Comparable) -> bool:
        return self.key_comparison() == other.key_comparison()

    def __ne__(self, other: Comparable) -> bool:
        return not self.key_comparison() == other.key_comparison()

    def __lt__(self, other: Comparable) -> bool:
        return self.key_comparison() < other.key_comparison()

    def __le__(self, other: Comparable) -> bool:
        return self.key_comparison() <= other.key_comparison()

    def __gt__(self, other: Comparable) -> bool:
        return self.key_comparison() > other.key_comparison()

    def __ge__(self, other: Comparable) -> bool:
        return self.key_comparison() >= other.key_comparison()
