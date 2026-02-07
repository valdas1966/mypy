from f_core.mixins.has.rows_cols import HasRowsCols
from f_core.mixins.has.name import HasName
from f_ds.grids.grid.base._select import Select
from f_ds.grids.cell import CellBase
from collections.abc import Iterable
from typing import Iterator, TypeVar, Generic, Type

Cell = TypeVar('Cell', bound=CellBase)


class GridBase(HasName,
               HasRowsCols,
               Iterable,
               Generic[Cell]):
    """
    ============================================================================
     2D-Grid Class of Cells.
    ============================================================================
    """

    # Factory
    Factory = None

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 type_cell: Type[Cell] = CellBase) -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        HasRowsCols.__init__(self, rows=rows, cols=cols)
        HasName.__init__(self, name=name)
        self._select = Select(grid=self)
        self._cells: list[list[Cell]] = self._init_cells(type_cell)

    @property
    def select(self) -> Select:
        """
        ========================================================================
         Return the Select object.
        ========================================================================
        """
        return self._select

    def neighbors(self, cell: Cell) -> list[Cell]:
        """
        ========================================================================
         Return the neighbors of a cell.
        ========================================================================
        """
        li: list[Cell] = []
        for row_col in cell.neighbors():
            row, col = row_col.to_tuple()
            if row < self.rows and col < self.cols:
                li.append(self[row][col])
        return li

    def _init_cells(self, type_cell: Type[Cell]) -> list[list[Cell]]:
        """
        ========================================================================
         Initialize the cells of the grid.
        ========================================================================
        """
        return [
                    [
                        type_cell(row, col) for col in range(self.cols)
                    ]
                    for row in range(self.rows)
                ]

    def __len__(self) -> int:
        """
        ========================================================================
         Return the total number of cells in the grid.
        ========================================================================
        """
        return self.rows * self.cols

    def __getitem__(self, index) -> list[Cell]:
        """
        ========================================================================
         1. Direct access to list Row of Cells via the [Row] Property.
         2. Direct access specific Cell using [Row][Col] Properties.
        ========================================================================
        """
        return self._cells[index]

    def __iter__(self) -> Iterator[Cell]:
        """
        ========================================================================
         Allow iteration over Cells in the Grid (flattened mode).
        ========================================================================
        """
        return (cell for row in self._cells for cell in row)
