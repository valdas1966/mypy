import numpy as np


class UArray:
    """
    ============================================================================
     Utility class for np arrays.
    ============================================================================
    """ 
    
    @staticmethod
    def remove_empty_rows(array: np.ndarray) -> np.ndarray:
        """
        ========================================================================
         Remove empty rows from a np array.
        ========================================================================
        """
        return np.array([row for row in array if row.any()])
    
    @staticmethod
    def remove_empty_columns(array: np.ndarray) -> np.ndarray:
        """
        ========================================================================
        Remove empty columns from a np array.
        ========================================================================
        """
        return array[:, np.any(array, axis=0)]
    
    @staticmethod
    def remove_empty_rows_and_columns(array: np.ndarray) -> np.ndarray:
        """
        ========================================================================
         Remove empty rows and columns from a np array.
        ========================================================================
        """
        array = UArray.remove_empty_rows(array=array)
        return UArray.remove_empty_columns(array=array)
