import numpy as np
import pytest
from f_psl.f_numpy.u_array import UArray


@pytest.fixture
def array() -> np.ndarray:
    """
    ========================================================================
     Create a boolean array with one empty row and one empty column.
    ========================================================================
    """
    return np.array([[True, False, False],
                     [True, True, False],
                     [False, False, False]])


def test_remove_empty_rows(array: np.ndarray) -> None:
    """
    ========================================================================
     Test the remove_empty_rows() method.
    ========================================================================
    """
    result = UArray.remove_empty_rows(array=array)
    expected = np.array([[True, False, False],
                         [True, True, False]])
    assert np.array_equal(result, expected)


def test_remove_empty_columns(array: np.ndarray) -> None:
    """
    ========================================================================
     Test the remove_empty_columns() method.
    ========================================================================
    """
    result = UArray.remove_empty_columns(array=array)
    expected = np.array([[True, False],
                         [True, True],
                         [False, False]])
    assert np.array_equal(result, expected)


def test_remove_empty_rows_and_columns(array: np.ndarray) -> None:
    """
    ========================================================================
     Test the remove_empty_rows_and_columns() method.
    ========================================================================
    """
    result = UArray.remove_empty_rows_and_columns(array=array)
    expected = np.array([[True, False],
                         [True, True]])
    assert np.array_equal(result, expected)


def test_generate_bins() -> None:
    """
    ========================================================================
     Test generate_bins() with n=3 on range [1..10].
    ========================================================================
    """
    values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    result = UArray.generate_bins(values=values, n=3)
    assert result == [1, 6, 10]


def test_generate_bins_n_5() -> None:
    """
    ========================================================================
     Test generate_bins() with n=5 on range [0..100].
    ========================================================================
    """
    values = list(range(101))
    result = UArray.generate_bins(values=values, n=5)
    assert result == [0, 25, 50, 75, 100]


def test_snap_to_bins() -> None:
    """
    ========================================================================
     Test snap_to_bins() with values [1..6] and bins [2, 4, 6].
    ========================================================================
    """
    values = np.array([1, 2, 3, 4, 5, 6])
    result = UArray.snap_to_bins(values=values, bins=[2, 4, 6])
    assert list(result) == [2, 2, 2, 4, 4, 6]


def test_snap_to_bins_single() -> None:
    """
    ========================================================================
     Test snap_to_bins() with a single bin.
    ========================================================================
    """
    values = np.array([1, 5, 10])
    result = UArray.snap_to_bins(values=values, bins=[5])
    assert list(result) == [5, 5, 5]


def test_snap_to_bins_exact() -> None:
    """
    ========================================================================
     Test snap_to_bins() when all values match bins exactly.
    ========================================================================
    """
    values = np.array([2, 4, 6])
    result = UArray.snap_to_bins(values=values, bins=[2, 4, 6])
    assert list(result) == [2, 4, 6]
