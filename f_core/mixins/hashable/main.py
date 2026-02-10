from f_core.mixins.equatable import Equatable


class Hashable(Equatable):
    """
    ============================================================================
     Mixin for hashable objects (has distinct value for each instance).
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
        return hash(self.key_comparison())
