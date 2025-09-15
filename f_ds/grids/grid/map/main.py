from f_ds.grids.grid.base.main import GridBase
from f_ds.grids.cell import CellMap
from f_ds.groups.view import View


class GridMap(GridBase[CellMap]):
    """
    ============================================================================
     2D-Grid Class of CellsMaps (can be valid or invalid).
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
        
    def cells_valid(self) -> list[CellMap]:
        """
        ========================================================================
         Return a View of the Valid Cells in the Grid.
        ========================================================================
        """
        return [cell for cell in self if cell]
    
    def neighbors(self, cell: CellMap) -> list[CellMap]:
        """
        ========================================================================
         Return the neighbors of a cell.
        ========================================================================
        """
        li: list[CellMap] = list()
        for cell in GridBase.neighbors(self, cell=cell):
            if cell:
                li.append(cell)
        return li

    def __str__(self) -> str:
        """
        ========================================================================
         Return a String Representation of the Grid in [0,1] 2Dbool format:
         [ Name of the Grid [Shape]]
            [0, 1, 0],
            [1, 0, 1],
            [0, 1, 0]
         ]
        ========================================================================
        """
        title = f'{self.name} {self.shape()}'
        matrix = '\n'.join([' '.join(['1' if cell else '0' for cell in row]) for row in self._cells])
        return f'{title}\n{matrix}'
