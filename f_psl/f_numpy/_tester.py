from f_psl.f_numpy.u_array import UArray, np
import pytest


@pytest.fixture
def array() -> np.ndarray:
    """
    ========================================================================
     Array to test.
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
    array_test = UArray.remove_empty_rows(array=array)
    array_true = np.array([[True, False, False],
                           [True, True, False]])
    assert np.array_equal(array_test, array_true)
    
    
def test_remove_empty_columns(array: np.ndarray) -> None:
    """
    ========================================================================
     Test the remove_empty_columns() method.
    ========================================================================
    """ 
    array_test = UArray.remove_empty_columns(array=array)
    array_true = np.array([[True, False],
                           [True, True],
                           [False, False]])
    assert np.array_equal(array_test, array_true)
    
    
def test_remove_empty_rows_and_columns(array: np.ndarray) -> None:
    """
    ========================================================================
     Test the remove_empty_rows_and_columns() method.
    ========================================================================
    """
    array_test = UArray.remove_empty_rows_and_columns(array=array)  
    array_true = np.array([[True, False],
                           [True, True]])
    assert np.array_equal(array_test, array_true)
