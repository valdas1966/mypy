from __future__ import annotations
from f_core.protocols.equable import Equable
from typing import Protocol


class Comparable(Protocol, Equable):
    """
    ============================================================================
     Protocol that supports comparable-methods.
    ============================================================================
    """

    def __lt__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the Object is less than the other Object.
        ========================================================================
        """

    def __le__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the Object is less or equal to the other Object.
        ========================================================================
        """

    def __gt__(self, other: object) -> bool:
        """
        ========================================================================
         Return True if the Object is greater than the other Object.
        ========================================================================
        """

    def __ge__(self, other: object) -> bool:
        """
        ========================================================================
         Return True if the Object is greater or equal to the other Object.
        ========================================================================
        """
