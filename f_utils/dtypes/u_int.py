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
    def rel_to_abs(rel: int, total: int) -> int:
        """
        ========================================================================
         Convert a Relative val [0,100] to an Absolute val based on the Total.
        ========================================================================
        """
        return int(rel / 100 * total)

    @staticmethod
    def dims_rel_to_abs(x: int,
                        y: int,
                        width: int,
                        height: int,
                        total_width: int,
                        total_height: int) -> tuple[int, int, int, int]:
        """
        ========================================================================
         Convert Relative dimension to Absolute values.
        ========================================================================
        """
        abs_x = UInt.rel_to_abs(x, total_width)
        abs_y = UInt.rel_to_abs(y, total_height)
        abs_width = UInt.rel_to_abs(width, total_width)
        abs_height = UInt.rel_to_abs(height, total_height)
        return abs_x, abs_y, abs_width, abs_height
