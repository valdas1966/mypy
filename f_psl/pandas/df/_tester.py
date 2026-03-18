import pandas as pd
from f_psl.pandas.df import UDf


def test_group_mean():
    """
    ========================================================================
     Test group() with mean aggregation.
    ========================================================================
    """
    df = pd.DataFrame({'a': [1, 1, 2, 2], 'b': [10, 20, 30, 40]})
    result = UDf.group(df=df, col_a='a', col_b='b', agg='mean')
    assert list(result['a']) == [1, 2]
    assert list(result['b']) == [15.0, 35.0]


def test_group_sum():
    """
    ========================================================================
     Test group() with sum aggregation.
    ========================================================================
    """
    df = pd.DataFrame({'a': [1, 1, 2, 2], 'b': [10, 20, 30, 40]})
    result = UDf.group(df=df, col_a='a', col_b='b', agg='sum')
    assert list(result['a']) == [1, 2]
    assert list(result['b']) == [30, 70]


def test_group_count():
    """
    ========================================================================
     Test group() with count aggregation.
    ========================================================================
    """
    df = pd.DataFrame({'a': [1, 1, 2, 2, 2],
                       'b': [10, 20, 30, 40, 50]})
    result = UDf.group(df=df, col_a='a', col_b='b', agg='count')
    assert list(result['a']) == [1, 2]
    assert list(result['b']) == [2, 3]


def test_group_default_cols():
    """
    ========================================================================
     Test group() with default col_a and col_b (1st and 2nd columns).
    ========================================================================
    """
    df = pd.DataFrame({'a': [1, 1, 2, 2], 'b': [10, 20, 30, 40]})
    result = UDf.group(df=df, agg='mean')
    assert list(result['a']) == [1, 2]
    assert list(result['b']) == [15.0, 35.0]


def test_read_write(tmp_path):
    """
    ========================================================================
     Test read() and write() round-trip.
    ========================================================================
    """
    path = str(tmp_path / 'test.csv')
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    UDf.write(df=df, path=path)
    result = UDf.read(path=path)
    assert list(result['a']) == [1, 2]
    assert list(result['b']) == [3, 4]


def test_group_multi_cols():
    """
    ========================================================================
     Test group() with multiple col_b columns.
    ========================================================================
    """
    df = pd.DataFrame({'a': [1, 1, 2, 2],
                       'b': [10, 20, 30, 40],
                       'c': [100, 200, 300, 400]})
    result = UDf.group(df=df,
                       col_a='a',
                       col_b=['b', 'c'],
                       agg='mean')
    assert list(result['a']) == [1, 2]
    assert list(result['b']) == [15.0, 35.0]
    assert list(result['c']) == [150.0, 350.0]


def test_add_col_agg():
    """
    ========================================================================
     Test add_col_agg() with min, max, and sum functions.
    ========================================================================
    """
    df = pd.DataFrame({'a': [1, 5, 3], 'b': [4, 2, 6], 'c': [10, 20, 30]})
    # Min
    UDf.add_col_agg(df=df, cols=['a', 'b'], col='min', func=min)
    assert list(df['min']) == [1, 2, 3]
    # Max
    UDf.add_col_agg(df=df, cols=['a', 'b'], col='max', func=max)
    assert list(df['max']) == [4, 5, 6]
    # Sum across 3 columns
    UDf.add_col_agg(df=df, cols=['a', 'b', 'c'], col='total', func=sum)
    assert list(df['total']) == [15, 27, 39]
