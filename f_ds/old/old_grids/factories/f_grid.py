import numpy as np
from f_ds.old.old_grids.old_grid import Grid


class FactoryGrid:

    @classmethod
    def from_array(cls, array: np.ndarray, name: str = None) -> Grid:
        """
        ========================================================================
         Create a Grid from a np boolean array.
        ========================================================================
        """
        rows = array.shape[0]
        cols = array.shape[1]
        grid = Grid(name=name, rows=rows, cols=cols)
        for row in range(rows):
            for col in range(cols):
                if not array[row][col]:
                    grid[row][col].set_invalid()
        return grid

    