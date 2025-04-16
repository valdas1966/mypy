from f_const.enums.types import TypeComparison
from f_psl.pandas.u_series import USeries
from itertools import product
import pandas as pd


class TypeAgg:
    """
    ============================================================================
        Type of Aggregation.
    ============================================================================
    """
    MEAN = 'mean'
    MEDIAN = 'median'
    SUM = 'sum'
    MIN = 'min'
    MAX = 'max'


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

    @staticmethod
    def agg_cols(df: pd.DataFrame,
                 cols: list[str],
                 type_agg: TypeAgg = TypeAgg.MEAN) -> list[float]:
        """
        ========================================================================
         Aggregate the values of the columns in the list.
        ------------------------------------------------------------------------
         Example:
         df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [6, 7, 8, 9, 10]})
         UDF.agg_cols(df=df, cols=['a', 'b'], type_agg=TypeAgg.MEAN)
         Output: [3.0, 8.0]
        ========================================================================
        """
        agg: pd.Series = None
        match type_agg:
            case TypeAgg.MEAN:
                agg = df[cols].mean()
            case TypeAgg.MEDIAN:
                agg = df[cols].median()
            case TypeAgg.MIN:
                agg = df[cols].min()
            case TypeAgg.MAX:
                agg = df[cols].max()
            case TypeAgg.SUM:
                agg = df[cols].sum()
        return agg.tolist()
    
    @staticmethod
    def count_comparison(df: pd.DataFrame,
                         col_a: str,
                         col_b: str,
                         type_cmp: TypeComparison) -> int:
        """
        ========================================================================
         Count the number of rows where A [comparison] B.
        ========================================================================
         Example:
        ------------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 2, 3], 'b': [1, 1, 1]})
         UDF.count_comparison(df, 'a', 'b', TypeComparison.GREATER)
        ------------------------------------------------------------------------
         Output: 2
        ========================================================================
        """
        match type_cmp:
            case TypeComparison.GREATER:
                mask = df[col_a] > df[col_b]
            case TypeComparison.EQUAL:
                mask = df[col_a] == df[col_b]
            case TypeComparison.LESS:
                mask = df[col_a] < df[col_b]
            case TypeComparison.GREATER_EQUAL:
                mask = df[col_a] >= df[col_b]
            case TypeComparison.LESS_EQUAL:
                mask = df[col_a] <= df[col_b]
            case TypeComparison.NOT_EQUAL:
                mask = df[col_a] != df[col_b]
            case _:
                raise ValueError(f"Unsupported comparison: {type_cmp}")
        return mask.sum()


    @staticmethod
    def wide_to_long(df: pd.DataFrame,
                     col_x: str,
                     col_y: str,
                     cols_y: list[str],
                     col_val: str) -> pd.DataFrame:
        """
        ========================================================================
         Converts a wide-format DataFrame to a long format, using the index of
           each value column as the value for a new index column.
        ========================================================================
        """
        df_long = df.melt(id_vars=col_x, value_vars=cols_y,
                          var_name='temp_col', value_name=col_val)

        # Map column names to their position index (1-based)
        col_index_map = {col: idx + 1 for idx, col in enumerate(cols_y)}
        df_long[col_y] = df_long['temp_col'].map(col_index_map)

        df_long = df_long.drop(columns='temp_col')

        return df_long[[col_x, col_y, col_val]]
