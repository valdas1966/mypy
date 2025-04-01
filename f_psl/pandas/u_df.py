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
        df[col] = (round(df[col] / multiple) * multiple).astype(int)
        return df
