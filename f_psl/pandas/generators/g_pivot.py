from f_psl.pandas.u_pivot import UPivot
import pandas as pd
import numpy as np


class GenPivot:
    """
    ============================================================================
     Pivot Table Generator Class.
    ============================================================================
    """

    @staticmethod
    def window_full() -> pd.DataFrame:
        """
        ========================================================================
         Generate a pivot table for a full window.
        ========================================================================
        """
        x = [1, 2, 1, 2]
        y = [1, 1, 2, 2]
        val = [1, 2, 3, 4]
        df = pd.DataFrame({'x': x, 'y': y, 'val': val})
        return UPivot.from_df(df, col_x='x', col_y='y', col_val='val')

    @staticmethod
    def window_full_sum() -> pd.DataFrame:
        """
        ========================================================================
         Generate a pivot table for a full window with sum aggregation.
        ========================================================================
        """
        x = [1, 1, 2, 1, 2]
        y = [1, 1, 1, 2, 2]
        val = [1, 4, 2, 3, 4]
        df = pd.DataFrame({'x': x, 'y': y, 'val': val})
        return UPivot.from_df(df, col_x='x',
                              col_y='y',
                              col_val='val', 
                              func_agg=np.sum)
    
    @staticmethod
    def window_full_mean() -> pd.DataFrame:
        """
        ========================================================================
         Generate a pivot table for a full window with average aggregation.
        ========================================================================
        """
        x = [1, 1, 2, 1, 2]
        y = [1, 1, 1, 2, 2]
        val = [1, 5, 2, 3, 4]
        df = pd.DataFrame({'x': x, 'y': y, 'val': val})
        return UPivot.from_df(df, col_x='x',
                              col_y='y',
                              col_val='val', 
                              func_agg=np.mean)
    
    @staticmethod
    def window_broken() -> pd.DataFrame:
        """
        ========================================================================
         Generate a pivot table for a broken window.
        ========================================================================
        """
        x = [1, 2, 1]
        y = [1, 1, 2]
        val = [1, 2, 3]
        df = pd.DataFrame({'x': x, 'y': y, 'val': val})
        return UPivot.from_df(df, col_x='x',
                              col_y='y',
                              col_val='val')

