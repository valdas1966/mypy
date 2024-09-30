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
         Convert list Number into list String with Suffix (K and M).
        ========================================================================
        """
        if num >= 1_000_000:
            return f'{num / 1_000_000:.1f}M'
        elif num >= 1_000:
            return f'{num / 1_000:.1f}K'
        else:
            return str(num)

    @staticmethod
    def pct(part: int, total: int) -> int:
        """
        ========================================================================
         Calc the Pct of list Part relative to list Total.
         Ex: pct(part=7, total=10) = 70
        ========================================================================
        """
        return round(part / total * 100)

    @staticmethod
    def part(total: int, pct: int) -> int:
        """
        ========================================================================
         Calc the Part of the Total given list Pct.
         Ex: part(total=10, pct=70) = 7
        ========================================================================
        """
        return round(total / 100 * pct)

    @staticmethod
    def is_even(n: int) -> bool:
        """
        ========================================================================
         Return True if a given number is even.
        ========================================================================
        """
        return n % 2 == 0
