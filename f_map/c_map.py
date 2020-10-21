from f_utils import u_dict
from f_map.c_point import Point
from f_map.c_grid import Grid
from f_const.directions import Directions
from f_utils import u_random
import random


class Map(Grid):
    """
    ============================================================================
     Description: Represents 2D Grid Map.
    ============================================================================
    """

    def __init__(self, rows, cols=None, percent_blocks=0):
        """
        ========================================================================
         Description: Constructor.
        ========================================================================
         Arguments:
        ------------------------------------------------------------------------
            1. rows : int
            2. cols : int
            3. percent_blocks : int [0:100]
        ========================================================================
        """
        super().__init__(rows, cols)
        self.percent_blocks = percent_blocks



