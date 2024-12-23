from __future__ import annotations
from abc import ABC, abstractmethod
from f_core.protocols.equable import Equable as ProtocolEquable


class Equable(ABC):
    """
    ============================================================================
     Mixin for Objects that support Equality checks.
    ============================================================================
    """

    @abstractmethod
    def key_comparison(self) -> ProtocolEquable:
        """
        ========================================================================
         Return an Equable object
        ========================================================================
        """
        pass

    def __eq__(self, other: Equable) -> bool:
        """
        ========================================================================
         Return True if the current object is equal to another object.
        ========================================================================
        """
        return self.key_comparison() == other.key_comparison()

    def __ne__(self, other: Equable) -> bool:
        """
        ========================================================================
         Return True if the current object is not equal to another object.
        ========================================================================
        """
        return not self == other

    def __hash__(self) -> int:
        """
        ========================================================================
         Hash by Key-Comparison.
        ========================================================================
        """
        return hash(self.key_comparison())
