from __future__ import annotations
from f_core.mixins.has_name import HasName
from f_core.mixins.has_rows_cols import HasRowsCols
from f_ds.mixins.groupable import Groupable, Group
from f_ds.groups.view import View
from f_ds.grids.cell import Cell
from f_file.map_grid import MapGrid
from collections.abc import Iterable
from typing import Iterator, Callable
import numpy as np
import os


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

    def distance_avg(self, cells: Iterable[Cell]) -> int:
        """
        ========================================================================
         Return the average distance between all the cells in the iterable.
        ========================================================================
        """
        sum_dist = 0
        for cell in cells:
            for other in cells:
                if cell >= other:
                    continue
                sum_dist += self.distance(cell, other)
        return round(sum_dist / len(cells))
    
    def cells_within_distance(self,
                              cell: Cell,
                              distance_max: int,
                              distance_min: int = 0) -> list[Cell]:
        """
        ========================================================================
         Return list of valid Cells within a given Distance-Range. 
        ========================================================================
        """
        cells_within: list[Cell] = list()
        # Iterate only over relevant Rows
        row_min = max(0, cell.row - distance_max)
        row_max = min(self.rows, cell.row + distance_max + 1)
        for row in range(row_min, row_max):
            # Iterate only over relevant Cols
            col_min = max(0, cell.col - distance_max)
            col_max = min(self.cols, cell.col + distance_max + 1)
            for col in range(col_min, col_max):
                # 1. Skip the Cell itself
                if row == cell.row and col == cell.col:
                    continue
                cell_within = self._cells[row][col]
                # 2. Skip if Cell is not valid
                if not cell_within:
                    continue
                # 3. Skip if Distance is not within the given Range
                d = self.distance(cell, cell_within)
                print(cell.to_tuple(), cell_within.to_tuple(), distance_min, distance_max, d)
                if d < distance_min or d > distance_max:
                    continue
                # Add to List of Valid-Cells within Distance
                cells_within.append(cell_within)
        return cells_within
    
    def stam(self,
             cell: Cell,
             distance_max: int,
             distance_min: int = 0) -> list[Cell]:
        """
        ========================================================================
         Return list of valid Cells within a given Manhattan Distance-Range
         [distance_min, distance_max] from the given cell using an optimized
         diamond iteration.
        ========================================================================
        """
        cells_within: list[Cell] = []
        
        # Set the row bounds using distance_max and grid limits.
        row_start = max(0, cell.row - distance_max)
        row_end = min(self.rows - 1, cell.row + distance_max)
        
        for r in range(row_start, row_end + 1):
            dr = abs(r - cell.row)
            # Compute allowed column offset range for this row.
            lower_offset = max(0, distance_min - dr)
            upper_offset = distance_max - dr
            
            # If lower_offset > upper_offset, no valid column exists for this row.
            if lower_offset > upper_offset:
                continue
            
            for offset in range(lower_offset, upper_offset + 1):
                # When offset is 0, there's only one column candidate.
                if offset == 0:
                    # Skip the center cell.
                    if r == cell.row:
                        continue
                    c = cell.col
                    if 0 <= c < self.cols:
                        candidate = self._cells[r][c]
                        if candidate:
                            cells_within.append(candidate)
                else:
                    # Consider both the positive and negative offsets.
                    for c in (cell.col + offset, cell.col - offset):
                        if 0 <= c < self.cols:
                            candidate = self._cells[r][c]
                            if candidate:
                                cells_within.append(candidate)
        return cells_within

    
    def cells_within_percentile(self,
                                cell: Cell,
                                percentile_min: int = 0,
                                percentile_max: int = 100) -> list[Cell]:
        """
        ========================================================================
         Return list of valid Cells within a given Percentile.
        ========================================================================
        """
        n_cells_valid = len(self.cells_valid)
        distance_min = round(n_cells_valid * percentile_min / 100)
        distance_max = round(n_cells_valid * percentile_max / 100)
        print(len(self), n_cells_valid, distance_min, distance_max)
        return self.stam(cell=cell,
                         distance_min=distance_min,
                         distance_max=distance_max)
    
    def to_group(self, name: str = None) -> Group[Cell]:
        """
        ========================================================================
         Return list flattened list representation of the 2D Object.
        ========================================================================
        """
        return Group(name=name, data=list(self))
    
    def to_array(self) -> np.ndarray:
        """
        ========================================================================
         Return numpy boolean array representation of the Grid.
        ========================================================================
        """
        return np.array([[bool(cell) for cell in row]
                        for row in self._cells])
            
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
        Cell.invalidate(cells=cells_to_invalidate)
        return grid
    
    @classmethod
    def from_array(cls, array: np.ndarray, name: str = None) -> Grid:
        """
        ========================================================================
         Create a Grid from a numpy boolean array.
        ========================================================================
        """
        rows = array.shape[0]
        cols = array.shape[1]
        grid = Grid(name=name, rows=rows, cols=cols)
        for row in range(rows):
            for col in range(cols):
                if not array[row][col]:
                    grid[row][col].set_invalid()
        return grid

    @classmethod
    def from_map_grid(cls, path: str) -> Grid:
        """
        ========================================================================
         Create a Grid from a Map-Grid-File.
        ========================================================================
        """
        map_grid = MapGrid(path=path)
        name = os.path.splitext(os.path.basename(path))[0]
        array = map_grid.to_array()
        return cls.from_array(array=array, name=name)
