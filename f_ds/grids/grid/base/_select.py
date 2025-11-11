from f_ds.grids.grid.base.main import GridBase, Cell
from f_ds.groups.group import Group


class Select:
    """
    ============================================================================
     Select Class for GridBase.
    ============================================================================
    """

    def __init__(self,
                 grid: GridBase) -> None:
        """
        ========================================================================
         Initialize the Select object.
        ========================================================================
        """
        self._grid = grid

    def random(self, size: int = None, pct: int = None) -> Group[Cell]:
        """
        ========================================================================
         Return a random sample of Cells from the Grid.
        ========================================================================
        """
        return self._grid.sample(size=size, pct=pct)

    def random_in_range(self,
                        size: int = None,
                        pct: int = None,
                        row_min: int = 0,
                        col_min: int = 0,
                        row_max: int = None,
                        col_max: int = None) -> Group[Cell]:
        """
        ========================================================================
         Return a random sample of Cells from the Grid within a given range.
        ========================================================================
        """
        def predicate(cell: Cell) -> bool:
            is_valid_row = row_min <= cell.row <= row_max
            is_valid_col = col_min <= cell.col <= col_max
            return is_valid_row and is_valid_col
        cells_within = self._grid.filter(predicate=predicate)
        return cells_within.sample(size=size, pct=pct)


    def random_within_distance(self,
                               cell: Cell,
                               distance: int,
                               size: int = None,
                               pct: int = None) -> Group[Cell]:
        """
        ========================================================================
         Return a random sample of Cells from the Grid within a given distance from the given Cell.
        ========================================================================
        """
        offset = distance // 2
        row_min = max(cell.row - offset, 0)
        row_max = min(cell.row + offset, self._grid.rows - 1)
        col_min = max(cell.col - offset, 0)
        col_max = min(cell.col + offset, self._grid.cols - 1)
        return self.random_in_range(size=size,
                                    pct=pct,
                                    row_min=row_min,
                                    col_min=col_min,
                                    row_max=row_max,
                                    col_max=col_max)
