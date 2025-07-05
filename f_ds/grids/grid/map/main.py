from f_ds.grids.grid.base.main import GridBase
from f_ds.grids.cell import CellMap
from f_ds.groups.view import View


class GridMap(GridBase[CellMap]):
    """
    ============================================================================
     2D-Grid Class of Cells.
    ============================================================================
    """

    # Static Classes
    Factory: type = None
    From: type = None

    def __init__(self,
                 # Number of Rows in the Grid
                 rows: int,
                 # Number of Columns in the Grid (None -> Grid is a Square)
                 cols: int = None,
                 # Name of the Grid
                 name: str = 'GridMap') -> None:
        """
        ========================================================================
         Init private Attributes.
        ========================================================================
        """
        GridBase.__init__(self,
                          rows=rows,
                          cols=cols,
                          name=name,
                          type_cell=CellMap)
        
    def cells_valid(self) -> View[CellMap]:
        """
        ========================================================================
         Return a View of the Valid Cells in the Grid.
        ========================================================================
        """
        return View(group=self.to_group(),
                    predicate=bool)
    