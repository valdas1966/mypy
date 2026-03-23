import numpy as np


class UArray:
    """
    ============================================================================
     Utility class for NumPy array operations.
    ============================================================================
    """

    @staticmethod
    def remove_empty_rows(array: np.ndarray) -> np.ndarray:
        """
        ====================================================================
         Remove empty rows from a numpy array.
        ====================================================================
        """
        return np.array([row for row in array if row.any()])

    @staticmethod
    def remove_empty_columns(array: np.ndarray) -> np.ndarray:
        """
        ====================================================================
         Remove empty columns from a numpy array.
        ====================================================================
        """
        return array[:, np.any(array, axis=0)]

    @staticmethod
    def remove_empty_rows_and_columns(array: np.ndarray) -> np.ndarray:
        """
        ====================================================================
         Remove empty rows and columns from a numpy array.
        ====================================================================
        """
        array = UArray.remove_empty_rows(array=array)
        return UArray.remove_empty_columns(array=array)

    @staticmethod
    def generate_bins(values: list[int | float],
                      n: int) -> list[int]:
        """
        ====================================================================
         Generate n evenly-spaced integer bins spanning the range of
         values.
        --------------------------------------------------------------------
         Input:
        --------------------------------------------------------------------
         values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], n = 3
        --------------------------------------------------------------------
         Output:
        --------------------------------------------------------------------
         [1, 6, 10]
        ====================================================================
        """
        bins = np.linspace(start=min(values),
                           stop=max(values),
                           num=n)
        return list(np.round(bins).astype(int))

    @staticmethod
    def snap_to_bins(values: np.ndarray,
                     bins: list[int]) -> np.ndarray:
        """
        ====================================================================
         Snap each value to the nearest bin (ties go to lower bin).
        --------------------------------------------------------------------
         Input:
        --------------------------------------------------------------------
         values = [1, 2, 3, 4, 5, 6], bins = [2, 4, 6]
        --------------------------------------------------------------------
         Output:
        --------------------------------------------------------------------
         [2, 2, 2, 4, 4, 6]
        ====================================================================
        """
        bins_arr = np.array(sorted(bins))
        # Single bin — all values snap to it
        if len(bins_arr) == 1:
            return np.full_like(values, bins_arr[0])
        idx = np.searchsorted(a=bins_arr, v=values)
        idx = np.clip(idx, 1, len(bins_arr) - 1)
        left = bins_arr[idx - 1]
        right = bins_arr[idx]
        return np.where(values - left <= right - values,
                        left, right)
