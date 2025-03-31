from f_utils.dtypes.u_int import UInt
import pandas as pd


class UDF:
    """
    ============================================================================
     DataFrame Utility Class.
    ============================================================================
    """

    @staticmethod
    def format_col(df: pd.DataFrame,
                   col: str,
                   multiple: int) -> pd.DataFrame:
        """
        ========================================================================
        Format the column `col` to the nearest multiple.
        ========================================================================
        """
        df[col] = UInt.round_to_nearest_multiple(n=df[col],
                                                 multiple=multiple)
        return df
