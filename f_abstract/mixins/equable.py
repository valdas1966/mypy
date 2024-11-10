from __future__ import annotations
from abc import ABC, abstractmethod


class Equable(ABC):
    """
    ============================================================================
     Mixin for Objects that support Equality checks.
    ============================================================================
    """

    @abstractmethod
    def key_comparison(self) -> list:
        """
        ========================================================================
         Return a List that represents Key for Object-Comparison.
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
