from f_ds.old_grids.old_grid import Grid, Cell
from f_ds.groups.group import Group


class Select:
    """
    ============================================================================
     Select-Class for selecting Cells in a Grid.
    ============================================================================
    """

    def __init__(self, grid: Grid) -> None:
        """
        ========================================================================
         Initialize the Select-Class.
        ========================================================================
        """
        self._grid = grid

    def cells_within_distance(self,
                              # The anchor Cell
                              cell: Cell,
                              # The maximum distance from the anchor Cell
                              dist_max: int,
                              # The minimum distance from the anchor Cell
                              dist_min: int = 1) -> Group[Cell]:
        """
        ========================================================================
         Return a list of valid cells within a given Distance from
           the anchor Cell.
        ========================================================================
        """
        offset_row = self._offsets_cell_row(cell=cell,
                                            dist=dist_max)
        offset_col = self._offsets_cell_col(cell=cell,
                                            dist=dist_max)
        cells_within: list[Cell] = list()
        for d_col in range(offset_col[0], offset_col[1] + 1):
            for d_row in range(offset_row[0], offset_row[1] + 1):
                cell_within = self._cells[cell.row+d_row][cell.col+d_col]
                if not cell_within:
                    continue
                dist = self.distance(cell_a=cell, cell_b=cell_within)
                if dist_min <= dist <= dist_max:
                    cells_within.append(cell_within)
        return Group(name='Cells within Distance',
                     data=cells_within)
    
    def _offsets_cell_col(self,
                          cell: Cell,
                          dist: int) -> tuple[int, int]:
        """
        ========================================================================
         Return a tuple of the minimum and maximum offsets for the cell column
          based on a given distance range and a grid boundaries.
        ========================================================================
        """
        offset_min = max(-dist, -cell.col)
        offset_max = min(dist, self.cols - cell.col - 1)
        return offset_min, offset_max
    
    def _offsets_cell_row(self,
                          cell: Cell,
                          dist: int) -> tuple[int, int]:
        """ 
        ========================================================================
         Return a tuple of the minimum and maximum offsets for the cell row
          based on a given distance range and a grid boundaries.
        ========================================================================
        """
        offset_min = max(-dist, -cell.row)
        offset_max = min(dist, self.rows - cell.row - 1)
        return offset_min, offset_max
