import numpy as np


class Grid(np.ndarray):

    def __new__(cls, rows, cols=None, p_obstacles=0):
        """
        ========================================================================
         Description: Constructor.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. rows : int
            2. cols : int
            3. p_obstacles : int (Percent of Obstacles in Map [0:100])
        ========================================================================
        """
        if not cols:
            cols = rows
        return np.zeros(shape=(rows, cols), dtype=int)

