from f_core.protocols import SupportsEquality
from f_core.mixins import Equatable
from abc import abstractmethod


class Hashable(Equatable):
    """
    ============================================================================
     1. Mixin for objects that support hashing via the inherited key property.
     2. Guarantees: a == b implies hash(a) == hash(b).
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    @property
    @abstractmethod
    def key(self) -> SupportsEquality:
        """
        ========================================================================
         Return an object that supports equality checks.
        ========================================================================
        """
        raise NotImplementedError

    def __hash__(self) -> int:
        """
        ========================================================================
         Return the hash of the object.
        ========================================================================
        """
        return hash(self.key)
