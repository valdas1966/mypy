from typing import Protocol


class SupportsEquality(Protocol):
    """
    ============================================================================
     1. Protocol that supports equality checks between two objects.
     2. __ne__() is omitted; Python derives != from __eq__ by default.
    ============================================================================
    """

    def __eq__(self, other: object) -> bool:
        """
        ========================================================================
         Return True if the Object is equals to the other Object.
        ========================================================================
        """
