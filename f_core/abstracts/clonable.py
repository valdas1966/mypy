from __future__ import annotations
from abc import ABC, abstractmethod


class Clonable(ABC):
    """
    ============================================================================
     Clonable Abstract-Class.
    ============================================================================
    """

    @abstractmethod
    def clone(self) -> Clonable:
        """
        ========================================================================
         Clone an Object.
        ========================================================================
        """
