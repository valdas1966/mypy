from f_core.mixins.equatable import Equatable


class Hashable(Equatable):
    """
    ============================================================================
     1. Mixin for objects that support hashing via the inherited key property.
     2. Guarantees: a == b implies hash(a) == hash(b).
    ============================================================================
    """

    # Factory
    Factory: type | None = None

    def __hash__(self) -> int:
        """
        ========================================================================
         Return the hash of the object.
        ========================================================================
        """
        return hash(self.key)
