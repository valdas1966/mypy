from typing import Iterable


class UPercent:
    """
    ========================================================================
     Utility class for calculating percentages.
    ========================================================================
    """

    @staticmethod
    def to_pct(vals: Iterable[int],
               precision: int = 0) -> Iterable[int |float]:
        """
        ========================================================================
         Convert a list of integers to a list of percentages.
        ========================================================================
        """
        # Calculate the total sum of the list
        total = sum(vals)
        # If the total is 0, return a list of zeroes
        if not total:
            return [0] * len(vals)
        # Return the percentage of each value in the list relative to the total
        return [UPercent.pct_of(a=val, b=total, precision=precision)
                for val in vals]

    @staticmethod
    def pct_of(a: int, b: int, precision: int = 0) -> int | float:
        """
        ========================================================================
         Return the percentage of A relative to B.
        ========================================================================
        """
        if not b:
            raise ValueError('B cannot be 0', b)
        return round((a / b) * 100, precision)
