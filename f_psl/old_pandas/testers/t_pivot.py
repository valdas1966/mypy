from f_psl.pandas.generators.g_pivot import GenPivot
import pandas as pd
import numpy as np


def test_window_full():
    """
    ========================================================================
     Test the window full pivot table.
    ========================================================================
    """
    df = GenPivot.window_full()
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert df.index.tolist() == [1, 2]
    assert df.columns.tolist() == [1, 2]
    assert df.values.tolist() == [[1, 2], [3, 4]]


def test_window_full_sum():
    """
    ========================================================================
     Test the window full sum pivot table.
    ========================================================================
    """
    df = GenPivot.window_full_sum()
    assert df.values.tolist() == [[5, 2], [3, 4]]


def test_window_full_mean() -> None:
    """
    ========================================================================
     Test the window full mean pivot table.
    ========================================================================
    """
    df = GenPivot.window_full_mean()
    assert df.values.tolist() == [[3, 2], [3, 4]]


def test_window_broken() -> None:
    """
    ========================================================================
     Test the window broken pivot table.
    ========================================================================
    """
    df = GenPivot.window_broken()
    expected = pd.DataFrame([[1, 2], [3.0, np.nan]],
                            index=pd.Index([1, 2], name='y'),
                            columns=pd.Index([1, 2], name='x'))
    pd.testing.assert_frame_equal(df, expected)
