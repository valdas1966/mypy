from f_psl.pandas.generators.g_df import GenDF, pd
from f_psl.pandas.u_df import UDF, TypeAgg


def test_nearest_multiple() -> None:
    """
    ========================================================================
     Test the nearest_multiple() function.
    ========================================================================
    """
    df = GenDF.three_hands()
    d_cols = {'a': 2, 'b': 3}
    actual = UDF.nearest_multiple(df=df, d_cols=d_cols)
    a_expected = [2, 2, 4, 4, 6]
    b_expected = [0, 3, 3, 3, 6]
    c_expected = [1, 2, 3, 4, 5]
    data_expected = {'a': a_expected, 'b': b_expected, 'c': c_expected}
    expected = pd.DataFrame(data_expected)
    assert actual.equals(expected)


def test_add_values() -> None:
    """
    ========================================================================
     Test the add_values() function.
    ========================================================================
    """ 
    df = GenDF.two_hands()
    actual = UDF.add_values(df=df, col='a', values=[6])
    a_expected = [1, 2, 3, 4, 5, 6]
    b_expected = [1, 2, 3, 4, 5, None]
    data_expected = {'a': a_expected, 'b': b_expected}
    expected = pd.DataFrame(data_expected)
    assert actual.equals(expected)


def test_fill_missing_multiples() -> None:
    """
    ========================================================================
     Test the fill_missing_multiples() function.
    ========================================================================
    """
    df = GenDF.missing_multiples()
    df_actual = UDF.fill_missing_multiples(df=df,
                                           col_x='x',
                                           col_y='y',
                                           mult_x=2,
                                           mult_y=2)
    x_expected = [0, 0, 2, 2, 4, 4]
    y_expected = [0, 2, 0, 2, 0, 2]
    val_expected = [1, None, None, None, None, 2]
    data_expected = {'x': x_expected,
                     'y': y_expected,
                     'val': val_expected}
    df_expected = pd.DataFrame(data_expected)
    assert df_actual.equals(df_expected)


def test_agg_cols() -> None:
    """
    ========================================================================
     Test the agg_cols() function.
    ========================================================================
    """
    df = GenDF.two_hands()
    agg_min = UDF.agg_cols(df=df, cols=['a'], type_agg=TypeAgg.MIN)
    assert agg_min == [1]
    agg_max = UDF.agg_cols(df=df, cols=['a'], type_agg=TypeAgg.MAX)
    assert agg_max == [5]
    agg_mean = UDF.agg_cols(df=df, cols=['a'], type_agg=TypeAgg.MEAN)
    assert agg_mean == [3]
    agg_median = UDF.agg_cols(df=df, cols=['a'], type_agg=TypeAgg.MEDIAN)
    assert agg_median == [3]
    agg_sum = UDF.agg_cols(df=df, cols=['a'], type_agg=TypeAgg.SUM)
    assert agg_sum == [15]
    

def test_wide_to_long() -> None:
    """
    ========================================================================
     Test the wide_to_long() function.
    ========================================================================
    """
    df = GenDF.wide_to_long()
    actual = UDF.wide_to_long(df=df,
                              col_x='x',
                              col_y='y',
                              cols_y=['y_1', 'y_2'],
                              col_val='val')
    x_expected = [1, 2, 1, 2]
    y_expected = [1, 1, 2, 2]
    val_expected = [10, 20, 30, 40]
    data_expected = {'x': x_expected,
                     'y': y_expected,
                     'val': val_expected}
    expected = pd.DataFrame(data_expected)
    assert actual.equals(expected)
