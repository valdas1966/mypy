from __future__ import annotations
from f_core.mixins.equable import Equable


class Comparable(Equable):
    """
    ============================================================================
     Mixin class for objects that support comparison operations.
    ============================================================================
    """

    def __lt__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the current object is less than another object.
        ========================================================================
        """
        return self.key_comparison() < other.key_comparison()

    def __le__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the current object is less or equal to other object.
        ========================================================================
        """
        return self.key_comparison() <= other.key_comparison()

    def __gt__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the current object is greater that other object.
        ========================================================================
        """
        return self.key_comparison() > other.key_comparison()

    def __ge__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the current object is greater or equal to other object.
        ========================================================================
        """
        return self.key_comparison() >= other.key_comparison()
