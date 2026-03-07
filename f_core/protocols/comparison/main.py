from f_core.protocols.equality.main import SupportsEquality
from typing import Protocol


class SupportsComparison(SupportsEquality, Protocol):
    """
    ============================================================================
     1. Protocol that supports comparison operations (<, <=, >, >=).
     2. Concrete classes implement all operators explicitly via key.
    ============================================================================
    """

    def __lt__(self, other: object) -> bool:
        """
        ========================================================================
         Return True if the Object is less than the other Object.
        ========================================================================
        """
