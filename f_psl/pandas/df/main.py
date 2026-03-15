import pandas as pd


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
