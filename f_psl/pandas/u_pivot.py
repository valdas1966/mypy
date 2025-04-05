from f_psl.pandas.u_df import UDF
from f_psl.pandas.u_series import USeries
import pandas as pd
import numpy as np


class UPivot:
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
                mult_x: int = 1,
                mult_y: int = 1,
                func_agg: np.ufunc = np.sum) -> pd.DataFrame:
        """
        ========================================================================
         Create a pivot table from a dataframe.
        ========================================================================
        """
        # Create a new DF with specified columns to pivot
        cols = [col_x, col_y, col_val]
        df_pivot = df[cols]
        # Round the values of the columns to the nearest multiples
        d_cols = {col_x: mult_x, col_y: mult_y}
        df_mult = UDF.nearest_multiple(df=df_pivot, d_cols=d_cols)
        df_full = UDF.fill_missing_multiples(df=df_mult,
                                             col_x=col_x,
                                             col_y=col_y,
                                             mult_x=mult_x,
                                             mult_y=mult_y)
        # Pivot the df
        return pd.pivot_table(df_full,
                              index=col_y,
                              columns=col_x,
                              values=col_val,
                              aggfunc=func_agg)
