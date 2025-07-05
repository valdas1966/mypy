from .main import GridMap
import numpy as np


class From:
    """
    ============================================================================
     Create GridMaps from other Structures.
    ============================================================================
    """

    @staticmethod
    def array(array: np.ndarray) -> GridMap:
        """
        ========================================================================
         Return a GridMap from a boolean numpy array.
        ========================================================================
        """
        # Get the shape of the array
        rows = array.shape[0]
        cols = array.shape[1]
        # Create a GridMap with the same shape as the array
        grid = GridMap(rows=rows,
                       cols=cols)
        # Invalidate cells on False array values
        for i in range(rows):
            for j in range(cols):
                if not array[i][j]:
                    grid[i][j].set_invalid()
        # Return the GridMap that represents the boolean array
        return grid
