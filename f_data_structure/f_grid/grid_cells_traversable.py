from f_data_structure.f_grid.grid_cells import GridCells
from f_data_structure.f_grid.cell_traversable import CellTraversable
from f_data_structure.mixins.container_traversable import ContainerTraversable
from typing import Type, TYPE_CHECKING


if TYPE_CHECKING:
    class _IDETypeHints:
        def cells_traversable(self) -> list[CellTraversable]: pass
        def num_cells_traversable(self) -> int: pass
        def num_cells_not_traversable(self) -> int: pass
        def pct_cells_traversable(self) -> float: pass
        def pct_cells_not_traversable(self) -> float: pass


class GridCellsTraversable(GridCells, ContainerTraversable, _IDETypeHints):
    """
    ============================================================================
     Desc: Represents a Grid-Map of Traversable-Cells.
    ============================================================================
     Methods:
    ----------------------------------------------------------------------------
        1. cells_traversable_random() -> list[CellTraversable]
           - Returns Random-Traversable-Cells from the Grid.
    ============================================================================
     Methods from Mixin-ContainerTraversable:
    ----------------------------------------------------------------------------
        1. cells_traversable() -> list[CellTraversable]
           - Returns List of all Traversable-Cells in the Grid.
        2. num_cells_traversable() -> int
           - Returns a number of Traversable-Cells in the Grid.
        3. num_cells_not_traversable() -> int
           - Returns a number of Non-Traversable-Cells in the Grid.
        4. pct_cells_traversable() -> float
           - Returns a percentage of Traversable-Cells in the Grid.
        5. pct_cells_not_traversable() -> float
           - Returns a percentage of Non-Traversable-Cells in the Grid.
    ============================================================================
    """

    def __init__(self,
                 num_rows: int,
                 num_cols: int = None,
                 name: str = None,
                 class_cell: Type[CellTraversable] = CellTraversable,
                 ) -> None:
        GridCells.__init__(self, num_rows, num_cols, name, class_cell)
        ContainerTraversable.__init__(self, elements='cells')

    @classmethod
    def generate(cls,
                 num_rows: int,
                 num_cols: int = None,
                 pct_non_traversable: int = 0,
                 name: str = None) -> 'GridCellsTraversable':
        """
        ========================================================================
         Desc: Creates a GridCellsTraversable object with a received
                Percentage of non-traversable cells.
        ========================================================================
        """
        grid = cls(num_rows, num_cols, name)
        cells_random = grid.cells_random(pct=pct_non_traversable)
        for cell in cells_random:
            cell.is_traversable = False
        return grid
