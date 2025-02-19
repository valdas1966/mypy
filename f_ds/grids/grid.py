from __future__ import annotations
from f_core.mixins.has_name import HasName
from f_core.mixins.has_rows_cols import HasRowsCols
from f_ds.mixins.groupable import Groupable, Group
from f_ds.groups.view import View
from f_ds.grids.cell import Cell
from collections.abc import Iterable
from typing import Iterator, Callable


class Grid(HasName, HasRowsCols, Groupable[Cell], Iterable):
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
        HasName.__init__(self, name=name)
        HasRowsCols.__init__(self, rows=rows, cols=cols)
        self._cells = [
                        [Cell(row, col) for col in range(self.cols)]
                        for row in range(self.rows)
                      ]
        self._cells_valid = View(name='Valid Cells',
                                 group=self.to_group(),
                                 predicate=bool)

    @property
    def cells_valid(self) -> View[Cell]:
        """
        ========================================================================
         Component-Class for Valid-Cells in the Grid.
        ========================================================================
        """
        return self._cells_valid

    def neighbors(self, cell: Cell) -> list[Cell]:
        """
        ========================================================================
         Return List of list valid Cell-Neighbors in Clockwise-Order.
        ========================================================================
        """
        cells_within = [self._cells[n.row][n.col]
                        for n
                        in cell.neighbors()
                        if self.is_within(n.row, n.col)]
        return [cell for cell in cells_within if cell]

    def to_group(self, name: str = None) -> Group[Cell]:
        """
        ========================================================================
         Return list flattened list representation of the 2D Object.
        ========================================================================
        """
        return Group(name=name, data=list(self))

    def filter(self,
               predicate: Callable[[Cell], bool],
               name: str = None) -> Group[Cell]:
        """
        ========================================================================
         Return a Group of filtered Cells by a given Predicate.
        ========================================================================
        """
        return self.to_group().filter(predicate=predicate, name=name)
            
    @staticmethod
    def distance(cell_a: Cell, cell_b: Cell) -> int:
        """
        ========================================================================
         Return list Manhattan-Distance between the two given Cells.
        ========================================================================
        """
        diff_row = abs(cell_a.row - cell_b.row)
        diff_col = abs(cell_a.col - cell_b.col)
        return diff_row + diff_col

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 pct_valid: int = 100,
                 name: str = None) -> Grid:
        """
        ========================================================================
         Generate Grid with Random Valid-Cells based on list given Percentage.
        ========================================================================
        """
        grid = Grid(name=name, rows=rows, cols=cols)
        cells_to_invalidate = grid.sample(pct=100-pct_valid)
        Cell.invalidate(cells_to_invalidate)
        return grid

    def __getitem__(self, index) -> list[Cell]:
        """
        ========================================================================
         1. Direct access to list Row of Cells via the [Row] Property.
         2. Direct access specific Cell using [Row][Col] Properties.
        ========================================================================
        """
        return self._cells[index]

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
                res += '1 ' if self._cells[row][col] else '0 '
            res += '\n'
        return res

    def __iter__(self) -> Iterator[Cell]:
        """
        ========================================================================
         Allow iteration over Cells in the Grid (flattened mode).
        ========================================================================
        """
        return (cell for row in self._cells for cell in row)
