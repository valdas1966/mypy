from __future__ import annotations
from typing import Protocol


class Equable(Protocol):
    """
    ============================================================================
     Protocol that supports equality checks.
    ============================================================================
    """

    def __eq__(self, other: Equable) -> bool:
        """
        ========================================================================
         Return True if the Object is equals to the other Object.
        ========================================================================
        """

    def __ne__(self, other: Equable) -> bool:
        """
        ========================================================================
         Return False if the Object is equals to the other Object.
        ========================================================================
        """
