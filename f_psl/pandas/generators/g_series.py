import pandas as pd


class GenSeries:
    """
    ============================================================================
     Series Generator Class.
    ============================================================================
    """
    
    @staticmethod
    def five() -> pd.Series:
        """
        ========================================================================
        Generate a series of values that are the nearest multiple of 5.
        ========================================================================
        """
        vals = [1, 2, 3, 4, 5]
        return pd.Series(vals)
