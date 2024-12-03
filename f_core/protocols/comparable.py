from __future__ import annotations
from typing import Protocol


class Comparable(Protocol):
    """
    ============================================================================
     Protocol that supports comparable-methods.
    ============================================================================
    """

    def __eq__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return True if the Object is equals to the other Object.
        ========================================================================
        """

    def __ne__(self, other: Comparable) -> bool:
        """
        ========================================================================
         Return False if the Object is equals to the other Object.
        ========================================================================
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
