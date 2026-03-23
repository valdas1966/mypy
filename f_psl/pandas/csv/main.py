from collections.abc import Callable

from f_psl.pandas.df import UDf


class UCsv:
    """
    ============================================================================
     CSV Utility Class (pandas-powered CSV operations).
    ============================================================================
    """

    @staticmethod
    def group(path_input: str,
              path_output: str,
              col_a: str = None,
              col_b: str | list[str] = None,
              agg: str = 'mean') -> None:
        """
        ====================================================================
         Read CSV, group col_b by col_a, and write result to CSV.
         If col_a or col_b are None, use the 1st and 2nd columns.
        ====================================================================
        """
        df = UDf.read(path=path_input)
        df = UDf.group(df=df, col_a=col_a, col_b=col_b, agg=agg)
        UDf.write(df=df, path=path_output)

    @staticmethod
    def add_col_agg(path: str,
                    cols: list[str],
                    col: str,
                    func: Callable) -> None:
        """
        ====================================================================
         Read CSV, add a column by aggregating values across specified
         columns per row, and write result back.
        ====================================================================
        """
        df = UDf.read(path=path)
        UDf.add_col_agg(df=df, cols=cols, col=col, func=func)
        UDf.write(df=df, path=path)

    @staticmethod
    def union(path_1: str,
              path_2: str,
              path_output: str) -> None:
        """
        ====================================================================
         Read two CSVs, union them (UNION ALL), and write to output CSV.
        ====================================================================
        """
        df_1 = UDf.read(path=path_1)
        df_2 = UDf.read(path=path_2)
        df = UDf.union(df_1=df_1, df_2=df_2)
        UDf.write(df=df, path=path_output)

    @staticmethod
    def add_col_bins(path: str,
                     col: str,
                     bins: list[int] = None,
                     n: int = None) -> None:
        """
        ====================================================================
         Read CSV, add a 'binned_{col}' column by snapping values to
         the nearest bin, and write result back.
        ====================================================================
        """
        df = UDf.read(path=path)
        UDf.add_col_bins(df=df, col=col, bins=bins, n=n)
        UDf.write(df=df, path=path)
