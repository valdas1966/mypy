from __future__ import annotations
from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    # Only used for type hints
    from f_ds.grids.grid import Grid


class Factory:
    """
    ============================================================================
     Factory class for creating Grids.
    ============================================================================
    """

    @classmethod
    def array(cls,
              # The numpy boolean-array
              array: np.ndarray,
              # The name of the Grid
              name: str = None) -> Grid:
        """
        ========================================================================
         Create a Grid from a numpy boolean array.
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