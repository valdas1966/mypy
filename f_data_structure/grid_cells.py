from typing import List
from random import shuffle
from f_data_structure.interfaces.xyable import XYAble
from f_data_structure.grid import Grid
from f_data_structure.cell import Cell


class GridCells(Grid):
    """
    ============================================================================
     Desc: Represents a 2D-Grid of Cells with a given obstacle percentage.
           Returns a Cell element by index [x][y] if it is valid (traversable).
    ============================================================================
     Inherited Members:
    ----------------------------------------------------------------------------
        1. rows (int)              : Number of Grid's Rows.
        2. cols (int)              : Number of Grid's Columns.
        3. count_elements (int)    : Count of Grid's Elements.
    ----------------------------------------------------------------------------
        1. shape() -> str : Return a Grid's Shape in format (rows,cols).
    ============================================================================
     Members:
    ----------------------------------------------------------------------------
        1. percentage_obstacle (int)    : Percentage of obstacles in the Grid.
        2. count_obstacles (int)        : Count of Grid's Obstacles.
    ----------------------------------------------------------------------------
        1. elements() -> list[Cell] : Return list of traversable Cells.
        2. is_valid(x: int, y: int) -> bool : Return True if the coordinates
                                               are from traversable Cell.
    ============================================================================
    """

    def __init__(self,
                 rows: int,
                 cols: int = None,
                 percentage_obstacle: int = 0,
                 ) -> None:
        super().__init__(rows=rows, cols=cols, ele=Cell)
        self._percentage_obstacle = percentage_obstacle
        self._set_obstacles()

    @property
    def percentage_obstacle(self) -> int:
        return self._percentage_obstacle

    @property
    def count_obstacles(self) -> int:
        return self.rows * self.cols * self.percentage_obstacle // 100

    def _set_obstacles(self):
        """
        ========================================================================
         Desc: Set randomly [count_obstacles] Cells to be non-traversable.
        ========================================================================
        """
        cells = self.elements()
        shuffle(cells)
        for cell in cells[:self.count_obstacles]:
            cell.is_valid = False

    def cell(self, xy: XYAble):
        """
        ========================================================================
         Desc: Returns the Cell in XYAble position in the Grid.
        ========================================================================
        """
        return self._grid[xy.x][xy.y]

    def is_valid(self,
                 x: int = None,
                 y: int = None,
                 xy: XYAble = None) -> bool:
        """
        ========================================================================
         Desc: Check if the given (X,Y) Coordinates are valid in the Grid
                and the Cell at these coordinates is also valid (traversable).
        ========================================================================
        """
        if not isinstance(x, int):
            x, y = xy.x, xy.y
        is_valid_coord = super().is_valid(x, y)
        if is_valid_coord:
            return self._grid[x][y].is_valid
        return False
