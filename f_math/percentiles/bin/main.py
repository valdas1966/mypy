from f_core.mixins.has.key import HasKey


class Bin(HasKey[int]):
    """
    ============================================================================
     Represents a percentile bin with lower and upper bounds.
     The key is the upper percentile (e.g., 10, 20, ..., 100).
    ============================================================================
    """

    def __init__(self,
                 percentile: int,
                 lower: int,
                 upper: int) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        # Upper percentile of the bin (e.g., 10, 20, ..., 100)
        HasKey.__init__(self, key=percentile)
        # Lower bound (inclusive)
        self._lower = lower
        # Upper bound (exclusive)
        self._upper = upper

    @property
    def lower(self) -> int:
        """
        ========================================================================
         Return the lower bound (inclusive).
        ========================================================================
        """
        return self._lower

    @property
    def upper(self) -> int:
        """
        ========================================================================
         Return the upper bound (exclusive).
        ========================================================================
        """
        return self._upper

    @property
    def percentile(self) -> int:
        """
        ========================================================================
         Return the upper percentile of this bin (alias for key).
        ========================================================================
        """
        return self._key

    def __contains__(self, value: int) -> bool:
        """
        ========================================================================
         Check if a value falls within this bin [lower, upper).
        ========================================================================
        """
        return self._lower <= value < self._upper

    def __repr__(self) -> str:
        """
        ========================================================================
         String representation of the bin.
        ========================================================================
        """
        str_range = f"[{self._lower}, {self._upper})"
        return f"Bin(percentile={self._key}, range={str_range})"
