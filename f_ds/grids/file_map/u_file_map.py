from f_psl.file import UTxt
import numpy as np


class UFileMap:
    """
    ============================================================================
     Utility class for file-maps.
    ============================================================================
    """
    
    @staticmethod
    def to_bool_array(path: str) -> np.ndarray:
