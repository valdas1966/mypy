from f_psl.pandas.generators.g_series import GenSeries
from f_psl.pandas.u_series import USeries
import pandas as pd


def test_nearest_multiple() -> None:
    """
    ========================================================================
    Test the nearest_multiple() function.
    ========================================================================
    """
    five = GenSeries.five()
    actual = USeries.nearest_multiple(series=five, multiple=3)
    expected = pd.Series([0, 3, 3, 3, 6])
    assert actual.equals(expected)


def test_missing_multiples() -> None:
    """
    ========================================================================
    Test the missing_multiples() function.
    ========================================================================
    """ 
    series = pd.Series([1, 8])
    actual = USeries.missing_multiples(series=series, multiple=3)
    expected = [3, 6]
    assert actual == expected


def test_to_df() -> None:
    """
    ========================================================================
    Test the to_df() function.
    ========================================================================
    """
    series = pd.Series(name='a', data=[11, 22])
    actual = USeries.to_df(series=series, col_b='b')
    expected = pd.DataFrame({'a': [0, 1], 'b': [11, 22]})
    assert actual.equals(expected)


def test_cnt() -> None:
    """
    ========================================================================
     Test the count() function.
    ========================================================================
    """
    series = GenSeries.fibonacci(n=3)
    actual = USeries.cnt(series=series)
    expected = pd.DataFrame({'val': [1, 0], 'cnt': [2, 1]})
    assert actual.equals(expected)


def test_pct() -> None:
    """
    ========================================================================
     Test the pct() function.
    ========================================================================
    """
    series = GenSeries.fibonacci(n=4)   
    actual = USeries.pct(series=series)
    expected = pd.DataFrame({'val': [1, 0, 2], 'pct': [50, 25, 25]})
    assert actual.equals(expected)

