from __future__ import annotations
from abc import abstractmethod
from f_core.mixins.equable import Equable, ProtocolEquable


class Comparable(Equable):
    """
    ============================================================================
     Mixin class for objects that support comparison operations.
    ============================================================================
    """

    # Factory
    Factory: type = None

    @abstractmethod
    def key_comparison(self) -> ProtocolEquable:
        """
        ========================================================================
         Return the key for comparison between two Comparable objects.
        ========================================================================
        """
        pass

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
