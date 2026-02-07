from f_core.protocols.equality.main import SupportsEquality
from abc import abstractmethod


class Equable(SupportsEquality):
    """
    ============================================================================
     1. Mixin for Objects that support Equality checks.
     2. __ne__() is omitted because Python automatically implements it as
       `not self == other`.
    ============================================================================
    """

    # Factory
    Factory: type | None= None

    @abstractmethod
    def key_comparison(self) -> SupportsEquality:
        """
        ========================================================================
         Return an object that supports equality checks.
        ========================================================================
        """
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """
        ========================================================================
         Return True if the current object is equal to another object.
        ========================================================================
        """
        if other is self:
            return True
        if not isinstance(other, Equable):
            return NotImplemented
        return self.key_comparison() == other.key_comparison()
