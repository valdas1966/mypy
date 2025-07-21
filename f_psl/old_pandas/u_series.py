from f_psl.math.u_multiple import UMultiple
from f_utils.dtypes.u_int import UInt
import pandas as pd


class USeries:
    """
    ============================================================================
     Series Utility Class.
    ============================================================================
    """
    
    @staticmethod
    def min_max(series: pd.Series) -> tuple[int, int]:
        """
        ========================================================================
        Return the minimum and maximum values of the series.
        ========================================================================
        """
        return series.min(), series.max()

    @staticmethod
    def nearest_multiple(series: pd.Series,
                         multiple: int) -> pd.Series:
        """
        ========================================================================
        Round the values of the series to the nearest multiple of `multiple`.
        ========================================================================
        """
        if multiple is None:
            return series
        return series.apply(lambda x: UMultiple.nearest(x, multiple))

    @staticmethod
    def missing_multiples(series: pd.Series,
                          multiple: int) -> list[int]:
        """
        ========================================================================
         Return a list of missing multiples of the series.
        ------------------------------------------------------------------------
         Input:
        ------------------------------------------------------------------------
         series = pd.Series([1, 8])
         multiple = 3
         missing = USeries.missing_multiples(series=series,
                                             multiple=multiple)
         print(missing)
        ------------------------------------------------------------------------
         Output: [3, 6]
        ========================================================================
        """ 
        # Get the min and max values of the series
        val_min, val_max = USeries.min_max(series=series)

        # Get the nearest multiple of the min and max values
        multiple_min = UMultiple.nearest(val_min, multiple)
        multiple_max = UMultiple.nearest(val_max, multiple)

        # Generate expected full set of multiples
        val_from = multiple_min
        val_to = multiple_max + multiple
        step = multiple
        expected = set(range(val_from, val_to, step))

        # Align each series value to its nearest multiple
        actual = set(UMultiple.nearest(v, multiple)
                     for v in series)

        # Return sorted list of missing aligned multiples
        missing = sorted(expected - actual)
        return missing

    @staticmethod
    def cnt(series: pd.Series) -> pd.DataFrame:
        """
        ========================================================================
         Count the number of occurrences of each value in the series
          and return a DataFrame with the value and the count (descending).
        ========================================================================
         Input:
        ------------------------------------------------------------------------
         series = pd.Series(name='a', data=[1, 1, 2])
         df = USeries.cnt(series=series)
         print(df)
        ========================================================================
         Output:
        ------------------------------------------------------------------------
         a  cnt
         1   2
         2   1
        ========================================================================
        """
        # Get the counts of each value in the series
        s_counts = series.value_counts()
        # Convert the Series to a DataFrame (by resetting the index)
        df = USeries.to_df(series=s_counts, col_a=series.name, col_b='cnt')
        # Return the DataFrame
        return df

    @staticmethod
    def pct(series: pd.Series) -> pd.DataFrame:
        """
        ========================================================================
         Return a DataFrame with the percentage of occurrences of each value in
           the series (descending).
        ========================================================================
         Input:
        ------------------------------------------------------------------------
         series = pd.Series(name='a', data=[1, 1, 1, 2])
         df = USeries.pct(series=series)
         print(df)
        ========================================================================
         Output:
        ------------------------------------------------------------------------
         a  pct
         1  75
         2  25
        ========================================================================
        """
        # Get the counts of each value in the series
        s_counts = series.value_counts(normalize=True)
        # Mult the percentage by 100 and round to the nearest integer
        s_counts = s_counts.mul(100).round(0).astype(int)
        # Convert the Series to a DataFrame (by resetting the index)
        df = USeries.to_df(series=s_counts, col_a=series.name, col_b='pct')
        # Return the DataFrame
        return df

    @staticmethod
    def to_df(series: pd.Series,
              col_b: str,
              col_a: str = None) -> pd.DataFrame:
        """
        ========================================================================
         Convert a Series to a DataFrame.
        ========================================================================
        """
        # Convert the Series to a DataFrame (by resetting the index)
        df = series.reset_index()
        # Rename the columns
        col_a = col_a or series.name
        df.columns = [col_a, col_b]
        # Return the DataFrame
        return df
