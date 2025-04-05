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
                mult_x: int,
                mult_y: int,
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
        df_pivot = UDF.nearest_multiple(df=df_pivot, d_cols=d_cols)
        x_min = df_pivot[col_x].min()
        x_max = df_pivot[col_x].max()
        for x in range(x_min + mult_x, x_max, mult_x):
            if x not in df_pivot[col_x].values:
                # Add x-value to col_x
                df_pivot = pd.concat([df_pivot, pd.DataFrame({col_x: [x]})],
                                      ignore_index=True)
        df_pivot = df_pivot[df_pivot[col_x] == x]
        y_min = df_pivot[col_y].min()
        y_max = df_pivot[col_y].max()
            # pivot the df
        return pd.pivot_table(df_pivot,
                              index=d_cols['y'],
                              columns=d_cols['x'],
                              values=d_cols['val'],
                              aggfunc=func_agg,
                              index=[y_min, y_max],
                              columns=[x_min, x_max])
