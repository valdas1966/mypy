from enum import Enum
from abc import ABC


class Has(ABC):
    """
    ============================================================================
     Base-Class for Mixin-Classes that has some functionality.
    ============================================================================
    """

    @staticmethod
    def CL(self) -> Enum:
        pass
