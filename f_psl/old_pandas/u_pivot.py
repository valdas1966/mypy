import numpy as np
from f_psl.pandas.u_df import UDF
import pandas as pd


class UPivot:
    """
    ============================================================================
     Pivot Table Utility Class.
    ============================================================================
    """

    class TypeAgg:
        SUM = 'sum'
        MEAN = 'mean'
    
    @staticmethod
    def from_df(df: pd.DataFrame,
                col_x: str,
                col_y: str,
                col_val: str,
                mult_x: int = 1,
                mult_y: int = 1,
                type_agg: TypeAgg = TypeAgg.SUM) -> pd.DataFrame:
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
        # Define the aggregation function (None should be ignored)
        if type_agg == UPivot.TypeAgg.SUM:
            agg = lambda x: x.sum() if x.notna().any() else np.nan
        elif type_agg == UPivot.TypeAgg.MEAN:
            agg = lambda x: x.mean() if x.notna().any() else np.nan
        # Pivot the df
        return pd.pivot_table(df_full,
                              index=col_y,
                              columns=col_x,
                              values=col_val,
                              aggfunc=agg,
                              fill_value=None)
