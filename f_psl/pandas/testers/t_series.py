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
