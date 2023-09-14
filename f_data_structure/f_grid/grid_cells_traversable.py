from __future__ import annotations
from f_data_structure.f_grid.grid_cells import GridCells
from f_data_structure.f_grid.cell_traversable import CellTraversable
from typing import Type


class GridCellsTraversable(GridCells):
    """
    ============================================================================
     Desc: Represents a Grid-Map of Traversable-Cells.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. cells(only_traversable: bool = True) -> list[CellTraversable]
           [*] Returns List of Grid's Cells (Can return only Traversable).
        2. pct_cells_traversable() -> float
           [*] Returns Percentage of Traversable-Cells in the Grid.
    ============================================================================
     Class-Methods:
    ----------------------------------------------------------------------------
        1. generate(rows,
                    cols,
                    pct_non_traversable,
                    name) -> GridCellsTraversable
              [*] Generates a GridCellsTraversable object with a received
                   Percentage of non-traversable cells.
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 class_cell: Type[CellTraversable] = CellTraversable,
                 ) -> None:
        GridCells.__init__(self, rows, cols, name, class_cell)

    def cells(self, only_traversable: bool = True) -> list[CellTraversable]:
        """
        ========================================================================
         Desc: Returns List of Grid's Cells (Can return only Traversable).
        ========================================================================
        """
        res = super().cells()
        if only_traversable:
            res = [cell for cell in res if cell.is_traversable]
        return res

    def pct_cells_traversable(self) -> float:
        """
        ========================================================================
         Desc: Returns Percentage of Traversable-Cells in the Grid.
        ========================================================================
        """
        return len(self) / super().__len__()

    def __len__(self) -> int:
        """
        ========================================================================
         Desc: Returns the Number of Traversable-Cells in the Grid.
        ========================================================================
        """
        return len(self.cells())

    @classmethod
    def generate(cls,
                 rows: int,
                 cols: int = None,
                 name: str = None,
                 pct_non_traversable: int = 0
                 ) -> GridCellsTraversable:
        """
        ========================================================================
         Desc: Generates a GridCellsTraversable object with a received
                Percentage of non-traversable cells.
        ========================================================================
        """
        grid = cls(rows, cols, name)
        cells_random = grid.cells_random(pct=pct_non_traversable)
        for cell in cells_random:
            cell.is_traversable = False
        return grid
