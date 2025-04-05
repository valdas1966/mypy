import math


class UMultiple:
    """
    ============================================================================
     Math Utils-Class.
    ============================================================================
    """

    @staticmethod
    def nearest(n: int | float, mult: int | float) -> int | float:
        """
        ========================================================================
         Round the integer `n` to the nearest multiple of `mult`.
        ========================================================================
        """
        return int(math.floor(n / mult + 0.5) * mult)
