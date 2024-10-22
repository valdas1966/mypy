from __future__ import annotations
from abc import ABC, abstractmethod


class Equable(ABC):
    """
    ============================================================================
     Abstract-Class for Objects that supports Equality checks.
    ============================================================================
    """

    @abstractmethod
    def key_comparison(self) -> list:
        """
        ========================================================================
         Returns the Object's Key for Equality Comparison.
        ========================================================================
        """
        pass

    def __eq__(self, other: Equable) -> bool:
        """
        ========================================================================
         Return True if the Object is Equals to other Object.
        ========================================================================
        """
        return self.key_comparison() == other.key_comparison()

    def __ne__(self, other: Equable) -> bool:
        """
        ========================================================================
         Return True if the Object is not Equals to other Object.
        ========================================================================
        """
        return not self == other
