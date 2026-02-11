from __future__ import annotations
from abc import abstractmethod
from f_core.mixins.equatable.main import Equatable, ProtocolEquable


class Comparable(Equatable):
    """
    ============================================================================
     Mixin class for objects that support comparison operations.
    ============================================================================
    """

    @abstractmethod
    def key(self) -> ProtocolEquable:
        pass

    def __lt__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the current object is less than another object.
        ========================================================================
        """
        return self.key() < other.key()

    def __le__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the current object is less or equal to other object.
        ========================================================================
        """
        return self.key() <= other.key()

    def __gt__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the current object is greater that other object.
        ========================================================================
        """
        return self.key() > other.key()

    def __ge__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the current object is greater or equal to other object.
        ========================================================================
        """
        return self.key() >= other.key()
