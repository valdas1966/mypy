from f_ds.grids.grid.base.main import GridBase
from f_ds.grids.cell import CellMap as Cell
from f_ds.groups.group import Group


class GridMap(GridBase[Cell]):
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
                          type_cell=Cell)
        
    def cells_valid(self) -> list[Cell]:
        """
        ========================================================================
         Return a View of the Valid Cells in the Grid.
        ========================================================================
        """
        return [cell for cell in self if cell]
    
    def neighbors(self, cell: Cell) -> list[Cell]:
        """
        ========================================================================
         Return the neighbors of a cell.
        ========================================================================
        """
        li: list[Cell] = list[Cell]()
        for cell in GridBase.neighbors(self, cell=cell):
            if cell:
                li.append(cell)
        return li

    def to_group(self,
                 name: str = "Valid-Cells") -> Group:
        """
        ========================================================================
         Return a Group of the Grid's valid cells.
        ========================================================================
        """
        return Group[Cell](name=name, data=self.cells_valid())

    def __len__(self) -> int:
        """
        ========================================================================
         Return the total number of valid cells in the grid.
        ========================================================================
        """
        return len(self.cells_valid())

    def print(self) -> str:
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

    def __str__(self) -> str:
        """
        ========================================================================
         Return a String Representation of the Grid in [0,1] 2Dbool format:
         Tel-Aviv(3x3, 8)
        ========================================================================
        """
        return f'{self.name}({self.rows}x{self.cols}, {len(self)})'

    def __repr__(self) -> str:
        """
        ========================================================================
         Return a String Representation of the Grid in [0,1] 2Dbool format:
         <GridMap: Name=Tel-Aviv, Shape=3x3, Cells=8>
        ========================================================================
        """
        return f'<{type(self).__name__}: Name={self.name}, Shape={self.rows}x{self.cols}, Cells={len(self)}>'
