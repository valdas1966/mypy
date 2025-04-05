from f_psl.pandas.u_series import USeries
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
        df = pd.concat([df, pd.DataFrame({col: values})], ignore_index=True)
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
