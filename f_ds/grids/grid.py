from f_ds.collections.i_2d import Collection2D
from f_ds.grids.cell import Cell


class Grid(Collection2D[Cell]):

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None) -> None:
        Collection2D.__init__(self, name=name, rows=rows, cols=cols)
        self._items = [
                        [Cell(row, col)
                         for col in range(self.cols)]
                        for row in range(self.rows)
                        ]

    def neighbors(self, cell: Cell) -> list[Cell]:
        """
        ========================================================================
         Return List of a valid Cell-Neighbors in Clockwise-Order.
        ========================================================================
        """
        cells_within = [self._items[n.row][n.col] for n in cell.neighbors()]
        return [cell for cell in cells_within if cell.is_valid]

    def __getitem__(self, index) -> list[Cell]:
        """
        ========================================================================
         1. Direct access to a Row of Cells via the [Row] Property.
         2. Direct access specific Cell using [Row][Col] Properties.
        ========================================================================
        """
        return self._items[index]

    def __str__(self) -> str:
        """
        ========================================================================
         Plot the Grid with (0,1) values.
        ========================================================================
        """
        # Cols Title
        res = '  ' + ' '.join((str(col) for col in range(self.cols))) + '\n'
        for row in range(self.rows):
            res += str(row) + ' '
            for col in range(self.cols):
                res += '1 ' if self._grid[row][col].is_valid else '0 '
            res += '\n'
        return res
