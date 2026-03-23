from collections.abc import Callable

import pandas as pd

from f_psl.f_numpy.u_array import UArray


class UDf:
    """
    ============================================================================
     DataFrame Utility Class.
    ============================================================================
    """

    @staticmethod
    def read(path: str) -> pd.DataFrame:
        """
        ====================================================================
         Read a CSV file into a DataFrame.
        ====================================================================
        """
        return pd.read_csv(filepath_or_buffer=path)

    @staticmethod
    def write(df: pd.DataFrame, path: str) -> None:
        """
        ====================================================================
         Write a DataFrame to a CSV file.
        ====================================================================
        """
        df.to_csv(path_or_buf=path, index=False)

    @staticmethod
    def group(df: pd.DataFrame,
              col_a: str = None,
              col_b: str | list[str] = None,
              agg: str = 'mean') -> pd.DataFrame:
        """
        ====================================================================
         Group col_b by col_a with the specified aggregation function.
         If col_a is None, use the 1st column of df.
         If col_b is None, use the 2nd column of df.
         col_b can be a single column name or a list of column names.
        --------------------------------------------------------------------
         Input:
        --------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 1, 2, 2], 'b': [10, 20, 30, 40]})
         UDf.group(df=df, agg='mean')
        --------------------------------------------------------------------
         Output:
        --------------------------------------------------------------------
         a     b
         1  15.0
         2  35.0
        ====================================================================
        """
        cols = df.columns
        col_a = col_a or cols[0]
        col_b = col_b or cols[1]
        if isinstance(col_b, str):
            col_b = [col_b]
        return (df
                .groupby(col_a, as_index=False)
                .agg({col: agg for col in col_b}))

    @staticmethod
    def add_col_agg(df: pd.DataFrame,
                    cols: list[str],
                    col: str,
                    func: Callable) -> pd.DataFrame:
        """
        ====================================================================
         Add a column by aggregating values across specified columns
         per row using the given function.
        --------------------------------------------------------------------
         Input:
        --------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 5, 3], 'b': [4, 2, 6]})
         UDf.add_col_agg(df=df, cols=['a', 'b'], col='min', func=min)
        --------------------------------------------------------------------
         Output:
        --------------------------------------------------------------------
         a  b  min
         1  4    1
         5  2    2
         3  6    3
        ====================================================================
        """
        df[col] = df[cols].apply(func=func, axis=1)
        return df

    @staticmethod
    def union(df_1: pd.DataFrame,
              df_2: pd.DataFrame) -> pd.DataFrame:
        """
        ====================================================================
         Union two DataFrames with the same columns (UNION ALL).
        ====================================================================
        """
        return pd.concat(objs=[df_1, df_2], ignore_index=True)

    @staticmethod
    def add_col_bins(df: pd.DataFrame,
                 col: str,
                 bins: list[int] = None,
                 n: int = None) -> pd.DataFrame:
        """
        ====================================================================
         Add a 'binned_{col}' column by snapping each value to the
         nearest bin. Provide either explicit bins or n to auto-generate.
        --------------------------------------------------------------------
         Input:
        --------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 2, 3, 4, 5, 6]})
         UDf.add_col_bins(df=df, col='a', bins=[2, 4, 6])
        --------------------------------------------------------------------
         Output:
        --------------------------------------------------------------------
         a  binned_a
         1         2
         2         2
         3         2
         4         4
         5         4
         6         6
        ====================================================================
        """
        if n is not None:
            bins = UArray.generate_bins(values=df[col].tolist(),
                                        n=n)
        df[f'binned_{col}'] = UArray.snap_to_bins(
                                  values=df[col].values,
                                  bins=bins)
        return df

