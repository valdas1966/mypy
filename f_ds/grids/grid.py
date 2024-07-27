from f_abstract.components.stats_items import StatsItems
from f_abstract.mixins.has_rows_cols import HasRowsCols
from f_ds.collections.i_1d import Collection1D
from f_ds.grids.cell import Cell


class Grid(Collection1D[Cell], HasRowsCols):
    """
    ============================================================================
     2D-Grid Class of Cells.
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasRowsCols.__init__(self, rows=rows, cols=cols)
        items = [
                    [Cell(row, col) for col in range(self.cols)]
                    for row in range(self.rows)
                ]
        Collection1D.__init__(self, name=name, items=items)
        self._cells_valid = StatsItems(items=self.to_list(), predicate=bool)

    @property
    def cells_valid(self) -> StatsItems[Cell]:
        return self._cells_valid

    def to_list(self) -> list[Cell]:
        """
        ========================================================================
         Return a flattened list representation of the 2D Object.
        ========================================================================
        """
        return [cell for row in self._items for cell in row]

    @staticmethod
    def distance(cell_a: Cell, cell_b: Cell) -> int:
        """
        ========================================================================
         Return a Manhattan-Distance between the two given Cells.
        ========================================================================
        """
        diff_row = abs(cell_a.row - cell_b.row)
        diff_col = abs(cell_a.col - cell_b.col)
        return diff_row + diff_col

    def neighbors(self, cell: Cell) -> list[Cell]:
        """
        ========================================================================
         Return List of a valid Cell-Neighbors in Clockwise-Order.
        ========================================================================
        """
        cells_within = [self._items[n.row][n.col] for n in cell.neighbors()]
        return [cell for cell in cells_within if cell]

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
                res += '1 ' if self._items[row][col] else '0 '
            res += '\n'
        return res
