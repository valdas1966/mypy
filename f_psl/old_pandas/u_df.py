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
    COUNT = 'count'


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
        ------------------------------------------------------------------------    
         Input:
        ------------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 2], 'b': [11, 22]})
         df = UDF.add_values(df=df,
                             col='a',
                             values=[3])
         print(df)
        ------------------------------------------------------------------------
         Output:
        ------------------------------------------------------------------------
         a  b
         1  11
         2  22
         3  None
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
        ------------------------------------------------------------------------
         Input:
        ------------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [1, 2, 3, 4, 5]})
         d_cols = {'a': 2}
         UDF.nearest_multiple(df=df, d_cols=d_cols)
        ------------------------------------------------------------------------
         Output:
        ------------------------------------------------------------------------
         a  b
         2  1
         2  2
         4  3
         4  4
         6  5
        ========================================================================
        """
        for col, multiple in d_cols.items():
            df[col] = USeries.nearest_multiple(series=df[col],
                                               multiple=multiple)
        return df
    
    @staticmethod
    def fill_missing_multiples(df: pd.DataFrame,
                               col: str,
                               multiple: int) -> pd.DataFrame:
        """
        ========================================================================
         Fill missing multiples of the specified column.
        ------------------------------------------------------------------------
         Input:
        ------------------------------------------------------------------------
         df = pd.DataFrame({'a': [0, 9], 'b': [1, 2]})
         df = UDF.fill_missing_multiples(df=df,
                                         col='a',
                                         multiple=3)
         print(df)
        ------------------------------------------------------------------------
         Output:
        ------------------------------------------------------------------------
         a  b
         0  1
         3  None
         6  None
         9  2
        ========================================================================
        """
        # Get the missing multiples
        missing = USeries.missing_multiples(series=df[col],
                                            multiple=multiple)
        # Add the missing multiples to the DataFrame
        return UDF.add_values(df=df,
                              col=col,
                              values=missing)

    @staticmethod
    def fill_missing_multiple_pairs(df: pd.DataFrame,
                                    col_x: str,
                                    col_y: str,
                                    mult_x: int = 1,
                                    mult_y: int = 1) -> pd.DataFrame:
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
    def group_by_col(df: pd.DataFrame,
                     col: str,
                     as_index: bool = False) -> pd.core.groupby.DataFrameGroupBy:
        """
        ========================================================================
         Group the DataFrame by the specified column.
        ------------------------------------------------------------------------
         Input:
        ------------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 1, 2, 2], 'b': [1, 2, 3, 4]})
         for name, group in UDF.group_by_col(df=df, col='a'):
            print(name)
            print(group)
        ------------------------------------------------------------------------
         Output:
        ------------------------------------------------------------------------
         Group: 1
           a b
         0 1 1
         1 1 2
         Group: 2
           a b
         0 2 3
         1 2 4
        ========================================================================
        """
        return df.groupby(col, as_index=as_index)

    @staticmethod
    def agg_grouped_col(grouped: pd.core.groupby.DataFrameGroupBy,
                        col: str,
                        type_agg: TypeAgg = TypeAgg.MEAN) -> pd.DataFrame:
        """
        ========================================================================
         Aggregate the values of the column in the grouped DataFrame.
        ------------------------------------------------------------------------
         Input:
        ------------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 1, 2, 2], 'b': [1, 2, 3, 4]})
         grouped = UDF.group_by_col(df=df, col='a')
         UDF.agg_grouped_col(grouped=grouped, col='b', type_agg=TypeAgg.MEAN)
        ------------------------------------------------------------------------
         Output:
        ------------------------------------------------------------------------
         a  b
         1  1.5
         2  3.5
        ========================================================================
        """
        return grouped.agg({col: type_agg})

    @staticmethod
    def group_and_agg(df: pd.DataFrame,
                      col_group: str,
                      col_agg: str = None,
                      multiple_group: int = None,
                      type_agg: TypeAgg = TypeAgg.MEAN) -> pd.DataFrame:
        """
        ========================================================================
         Group the DataFrame by the specified columns.
        ------------------------------------------------------------------------
         Input:
        ------------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 2, 3, 4], 'b': [1, 2, 3, 4]})
         UDF.group_by(df=df,
                      col_group='a',
                      col_agg='b',
                      multiple_group=2,
                      type_agg=TypeAgg.MEAN)
        ------------------------------------------------------------------------
         Output:
        ------------------------------------------------------------------------
         a  b
         2  1.5
         4  3.5
        ========================================================================
        """ 
        # Round the values of the grouped column to the nearest multiple
        if multiple_group:
            df[col_group] = USeries.nearest_multiple(series=df[col_group],
                                                     multiple=multiple_group)
            df = UDF.fill_missing_multiples(df=df,
                                            col=col_group,
                                            multiple=multiple_group)
        # if col_agg is None, do: select col_group, count(*)
        if col_agg is None:
            df = USeries.pct(series=df[col_group])
            return df
        # Group the DataFrame by the specified column
        grouped = UDF.group_by_col(df=df, col=col_group)
        # Aggregate the values of the aggregated column
        return UDF.agg_grouped_col(grouped=grouped,
                                   col=col_agg,
                                   type_agg=type_agg)
    

    @staticmethod   
    def agg_cols(df: pd.DataFrame,
                 cols: list[str],
                 type_agg: TypeAgg = TypeAgg.MEAN) -> list[float]:
        """
        ========================================================================
         Aggregate the values of the columns in the list.
        ------------------------------------------------------------------------
         Input:
        ------------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 2, 3, 4, 5], 'b': [6, 7, 8, 9, 10]})
         UDF.agg_cols(df=df, cols=['a', 'b'], type_agg=TypeAgg.MEAN)
        ------------------------------------------------------------------------
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
            case TypeAgg.COUNT:
                agg = df[cols].count()
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
        ------------------------------------------------------------------------
         Example:
        ------------------------------------------------------------------------
         df = pd.DataFrame({'a': [1, 2, 3],
                            'b': [4, 5, 6],
                            'c': [7, 8, 9]})
         df = UDF.wide_to_long(df=df,
                               col_x='a',
                               col_y='b',
                               cols_y=['c'],
                               col_val='d')
        ------------------------------------------------------------------------
         Output:
        ------------------------------------------------------------------------
         a  b  c  d
         1  4  7  7
         2  5  8  8
         3  6  9  9
        ========================================================================
        """
        df_long = df.melt(id_vars=col_x, value_vars=cols_y,
                          var_name='temp_col', value_name=col_val)

        # Map column names to their position index (1-based)
        col_index_map = {col: idx + 1 for idx, col in enumerate(cols_y)}
        df_long[col_y] = df_long['temp_col'].map(col_index_map)

        df_long = df_long.drop(columns='temp_col')

        return df_long[[col_x, col_y, col_val]]
