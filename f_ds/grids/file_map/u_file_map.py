from f_psl.f_numpy import UArray
from f_psl.file import u_txt
import numpy as np


class UFileMap:
    """
    ============================================================================
     Utility class for file-maps.
    ============================================================================
    """

    _ROWS_TO_SKIP = 4
    _CHAR_VALID = '.'

    @staticmethod
    def to_bool_array_from_text(text: str) -> np.ndarray:
        """
        ========================================================================
         Parse a map-file body (as a string) into a boolean array. Keeps the
         same header-skip + valid-char semantics as to_bool_array(path).
        ========================================================================
        """
        lines = [line.strip() for line in text.splitlines()]
        lines = lines[UFileMap._ROWS_TO_SKIP:]
        array = np.array([[c == UFileMap._CHAR_VALID for c in line]
                          for line
                          in lines])
        return UArray.remove_empty_rows_and_columns(array=array)

    @staticmethod
    def to_bool_array(path: str) -> np.ndarray:
        """
        ========================================================================
         Convert a file-i_1_map on disk to a boolean array.
        ========================================================================
        """
        text = '\n'.join(u_txt.to_list(path=path))
        return UFileMap.to_bool_array_from_text(text=text)
