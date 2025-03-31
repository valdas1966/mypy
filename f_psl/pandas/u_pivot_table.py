import pandas as pd
import numpy as np


class UPivotTable:
    """
    ============================================================================
     Pivot Table Utility Class.
    ============================================================================
    """

    @staticmethod
    def from_df(df: pd.DataFrame,
                col_x: str,
                col_y: str,
                col_val: str,
                func_agg: np.ufunc = np.sum) -> pd.DataFrame:
        """
        ========================================================================
         Create a pivot table from a dataframe.
        ========================================================================
        """
        return pd.pivot_table(df,
                              index=col_y,
                              columns=col_x,
                              values=col_val,
                              aggfunc=func_agg)
