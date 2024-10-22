from __future__ import annotations
from abc import abstractmethod
from f_abstract.mixins.equable import Equable


class Comparable(Equable):
    """
    ============================================================================
     Mixin Comparable Class.
    ============================================================================
    """

    @abstractmethod
    def key_comparison(self) -> list:
        """
        ========================================================================
         Returns the Object's Key for Sorting.
        ========================================================================
        """
        pass

    def __lt__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the Object is less than other Object.
        ========================================================================
        """
        return self.key_comparison() < other.key_comparison()

    def __le__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the Object is less or equal to the other Object.
        ========================================================================
        """
        return self.key_comparison() <= other.key_comparison()

    def __gt__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the Object is greater than the other Object.
        ========================================================================
        """
        return self.key_comparison() > other.key_comparison()

    def __ge__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the Object is greater or equal to the other Object.
        ========================================================================
        """
        return self.key_comparison() >= other.key_comparison()
