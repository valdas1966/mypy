from f_psl.pandas.u_series import USeries
from itertools import product
import pandas as pd


class UDF:
    """
    ============================================================================
     DataFrame Utility Class.
    ============================================================================
    """

    @staticmethod
    def add_values(df: pd.DataFrame,
                   col: str,
                   values: list[any]) -> pd.DataFrame:
        """
        ========================================================================
         Add values to specified column.
        ========================================================================
        """
        df = pd.concat([df, pd.DataFrame({col: values})],
                        ignore_index=True)
        return df

    @staticmethod
    def nearest_multiple(df: pd.DataFrame,
                         d_cols: dict[str, int]) -> pd.DataFrame:
        """
        ========================================================================
         Round the values of the columns in the dict to the nearest multiple.
        ========================================================================
        """
        for col, multiple in d_cols.items():
            df[col] = USeries.nearest_multiple(series=df[col],
                                               multiple=multiple)
        return df
    
    @staticmethod    
    def fill_missing_multiples(df: pd.DataFrame,
                               col_x: str,
                               col_y: str,
                               mult_x: int,
                               mult_y: int) -> pd.DataFrame:
        """
        ========================================================================
         Add missing (x, y) multiple pairs to the DataFrame.
        ========================================================================
        """
        # Calc ranges of mult_x and mult_y
        x_min, x_max = df[col_x].min(), df[col_x].max()
        y_min, y_max = df[col_y].min(), df[col_y].max()

        # Generate full mult_x and mult_y ranges using step
        x_vals = list(range(x_min, x_max+1, mult_x))
        y_vals = list(range(y_min, y_max+1, mult_y))

        # Create full grid of (mult_x, mult_y)
        all_pairs = pd.DataFrame(product(x_vals, y_vals), columns=[col_x, col_y])

        # Merge with original df to preserve existing other cols values
        df_merged = pd.merge(all_pairs, df, on=[col_x, col_y], how='left')

        return df_merged
