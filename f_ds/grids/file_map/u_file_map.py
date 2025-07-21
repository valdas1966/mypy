from f_psl.f_numpy import UArray
from f_psl.file import UTxt
import numpy as np


class UFileMap:
    """
    ============================================================================
     Utility class for file-maps.
    ============================================================================
    """
    
    _ROWS_TO_SKIP = 4
    _CHAR_VALID = '_'
    
    @staticmethod
    def to_bool_array(path: str) -> np.ndarray:
        """
        ========================================================================
         Convert a file-map to a boolean array.
        ========================================================================
        """
        lines = UTxt.to_list(path=path)
        lines = lines[UFileMap._ROWS_TO_SKIP:]
        array = np.array([[c == UFileMap._CHAR_VALID for c in line]
                          for line
                          in lines])
        return UArray.remove_empty_rows_and_columns(array=array)
