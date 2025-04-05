from f_psl.math.u_multiple import UMultiple
import pandas as pd


class USeries:
    """
    ============================================================================
     Series Utility Class.
    ============================================================================
    """
    
    @staticmethod
    def nearest_multiple(series: pd.Series,
                         multiple: int) -> pd.Series:
        """
        ========================================================================
        Round the values of the series to the nearest multiple of `multiple`.
        ========================================================================
        """
        if multiple is None:
            return series
        return series.apply(lambda x: UMultiple.nearest(x, multiple))
