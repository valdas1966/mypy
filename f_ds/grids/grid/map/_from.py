from f_ds.grids.file_map import UFileMap
from .main import GridMap
import numpy as np


class From:
    """
    ============================================================================
     Create GridMaps from other Structures.
    ============================================================================
    """
    
    @staticmethod
    def file_map(path: str, name: str = None, domain: str = None) -> GridMap:
        """
        ========================================================================
         Return a GridMap created from a file-i_1_map.
        ========================================================================
        """
        # Get the boolean array from the file-i_1_map
        array = UFileMap.to_bool_array(path=path)
        # Return the GridMap
        return From.array(array=array, name=name, domain=domain)

    @staticmethod
    def array(array: np.ndarray, name: str = None, domain: str = None) -> GridMap:
        """
        ========================================================================
         Return a GridMap from a boolean np array.
        ========================================================================
        """
        # Get the shape of the array
        rows = array.shape[0]
        cols = array.shape[1]
        # Create a GridMap with the same shape as the array
        grid = GridMap(rows=rows,
                       cols=cols,
                       name=name,
                       domain=domain)
        # Invalidate cells on False array values
        for i in range(rows):
            for j in range(cols):
                if not array[i][j]:
                    grid[i][j].set_invalid()
        # Return the GridMap that represents the boolean array
        return grid
