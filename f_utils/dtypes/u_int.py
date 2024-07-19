class UInt:
    """
    ============================================================================
     Int Utils-Class.
    ============================================================================
    """

    @staticmethod
    def to_str(num: int) -> str:
        """
        ========================================================================
         Convert a Number into a String with Suffix (K and M).
        ========================================================================
        """
        if num >= 1_000_000:
            return f'{num / 1_000_000:.1f}M'
        elif num >= 1_000:
            return f'{num / 1_000:.1f}K'
        else:
            return str(num)

    @staticmethod
    def pct(val: int, total: int) -> int:
        """
        ========================================================================
         Calculate the Percentage of a Value relative to a Total.
        ========================================================================
        """
        return int(val / total * 100)
