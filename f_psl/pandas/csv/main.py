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
