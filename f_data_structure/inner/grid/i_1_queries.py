from f_data_structure.inner.grid.i_0_init import GridInit
from f_data_structure.xy import XY


class GridQueries(GridInit):

    def is_within(self,
                  x: int = None,
                  y: int = None,
                  xy: XY = None) -> bool:
        """
        ========================================================================
         Desc: Returns True if the Coordinates are within the Grid's Borders.
        ========================================================================
        """
        if xy:
            x, y = xy.x, xy.y
        is_x_valid = 0 <= x < self.num_rows
        is_y_valid = 0 <= y < self.num_cols
        return is_x_valid and is_y_valid
